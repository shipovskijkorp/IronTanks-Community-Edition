
package com.indemnity83.irontanks.common.block;

import buildcraft.factory.block.BlockTank;
import buildcraft.lib.tile.TileBC_Neptune;
import com.indemnity83.irontanks.common.blockentity.TankTile;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.BlockGetter;
import javax.annotation.Nullable;
import net.minecraft.world.level.block.state.BlockState;

import java.util.List;

public class TankBlock extends BlockTank {
    private static final int MILLIBUCKETS_PER_BUCKET = 1_000;
    private final int capacityBuckets;

    public TankBlock(int capacityBuckets, float hardness, float resistance) {
        super(defaultProperties().strength(hardness, resistance).requiresCorrectToolForDrops().noOcclusion());
        this.capacityBuckets = capacityBuckets;
    }

    public final int getCapacityBuckets() {
        return capacityBuckets;
    }

    public final int getCapacityMb() {
        return capacityBuckets * MILLIBUCKETS_PER_BUCKET;
    }

    @Override
    public TileBC_Neptune newBlockEntity(BlockPos pos, BlockState state) {
        return new TankTile(pos, state, getCapacityMb());
    }

    @Override
    public void appendHoverText(ItemStack stack, @Nullable BlockGetter level, List<Component> tooltip, TooltipFlag flag) {
        appendTankTooltip(tooltip);
    }

    private void appendTankTooltip(List<Component> tooltip) {
        tooltip.add(Component.translatable("irontanks.tooltip.capacity", capacityBuckets).withStyle(ChatFormatting.GRAY));
        appendExtraTooltip(tooltip);
    }

    protected void appendExtraTooltip(List<Component> tooltip) {
    }
}
