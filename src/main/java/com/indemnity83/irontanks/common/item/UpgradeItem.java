
package com.indemnity83.irontanks.common.item;

import buildcraft.factory.tile.TileTank;
import buildcraft.lib.tile.TileBC_Neptune;
import net.minecraft.core.BlockPos;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.properties.Property;

import java.util.function.Supplier;

public final class UpgradeItem extends Item {
    private final Supplier<? extends Block> upgradeFrom;
    private final Supplier<? extends Block> upgradeTo;

    public UpgradeItem(Properties properties, Supplier<? extends Block> upgradeFrom, Supplier<? extends Block> upgradeTo) {
        super(properties);
        this.upgradeFrom = upgradeFrom;
        this.upgradeTo = upgradeTo;
    }

    @Override
    public InteractionResult onItemUseFirst(ItemStack stack, UseOnContext context) {
        return tryUpgrade(context, stack);
    }

    @Override
    public InteractionResult useOn(UseOnContext context) {
        return tryUpgrade(context, context.getItemInHand());
    }

    private InteractionResult tryUpgrade(UseOnContext context, ItemStack heldStack) {
        Level level = context.getLevel();
        BlockPos pos = context.getClickedPos();
        BlockState oldState = level.getBlockState(pos);
        Block fromBlock = upgradeFrom.get();
        Block toBlock = upgradeTo.get();

        if (oldState.getBlock() != fromBlock) {
            return InteractionResult.PASS;
        }
        if (level.isClientSide) {
            return InteractionResult.SUCCESS;
        }
        if (!(level.getBlockEntity(pos) instanceof TileTank oldTank)) {
            return InteractionResult.PASS;
        }

        var fluid = oldTank.tank.getFluid().copy();
        BlockState newState = copySharedProperties(oldState, toBlock.defaultBlockState());
        if (!level.setBlock(pos, newState, Block.UPDATE_ALL)) {
            return InteractionResult.FAIL;
        }

        if (!(level.getBlockEntity(pos) instanceof TileTank newTank)) {
            level.setBlock(pos, oldState, Block.UPDATE_ALL);
            if (level.getBlockEntity(pos) instanceof TileTank restoredTank) {
                restoredTank.tank.setFluid(fluid);
                restoredTank.setChanged();
                restoredTank.sendNetworkUpdate(TileBC_Neptune.NET_RENDER_DATA);
            }
            return InteractionResult.FAIL;
        }

        if (!fluid.isEmpty()) {
            newTank.tank.setFluid(fluid);
            newTank.balanceTankFluids();
        }
        newTank.setChanged();
        newTank.sendNetworkUpdate(TileBC_Neptune.NET_RENDER_DATA);

        Player player = context.getPlayer();
        if (player == null || !player.getAbilities().instabuild) {
            heldStack.shrink(1);
        }
        return InteractionResult.CONSUME;
    }

    private static BlockState copySharedProperties(BlockState source, BlockState target) {
        for (Property<?> property : source.getProperties()) {
            if (target.hasProperty(property)) {
                target = copyProperty(source, target, property);
            }
        }
        return target;
    }

    private static <T extends Comparable<T>> BlockState copyProperty(BlockState source, BlockState target, Property<T> property) {
        return target.setValue(property, source.getValue(property));
    }
}
