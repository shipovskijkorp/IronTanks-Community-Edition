
package com.indemnity83.irontanks.common.block;

import buildcraft.lib.tile.TileBC_Neptune;
import com.indemnity83.irontanks.common.blockentity.VoidTankTile;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.world.level.block.state.BlockState;

import java.util.List;

public final class VoidTankBlock extends StackableTankBlock {
    public VoidTankBlock(int capacityBuckets, float hardness, float resistance) {
        super(capacityBuckets, hardness, resistance);
    }

    @Override
    public TileBC_Neptune newBlockEntity(BlockPos pos, BlockState state) {
        return new VoidTankTile(pos, state, getCapacityMb());
    }

    @Override
    protected void appendExtraTooltip(List<Component> tooltip) {
        tooltip.add(Component.translatable("irontanks.tooltip.void_tank").withStyle(ChatFormatting.DARK_PURPLE));
    }
}
