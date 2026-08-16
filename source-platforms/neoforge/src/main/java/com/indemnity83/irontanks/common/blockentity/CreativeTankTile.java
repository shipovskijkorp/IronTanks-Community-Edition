
package com.indemnity83.irontanks.common.blockentity;

import buildcraft.factory.tile.TileTank;
import com.indemnity83.irontanks.common.registry.IronTanksBlockEntities;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.level.block.state.BlockState;

import net.neoforged.neoforge.fluids.FluidStack;
import net.neoforged.neoforge.fluids.capability.IFluidHandler.FluidAction;

public final class CreativeTankTile extends TankTile {
    public CreativeTankTile(BlockPos pos, BlockState state) {
        this(pos, state, capacityFromState(state));
    }

    public CreativeTankTile(BlockPos pos, BlockState state, int capacityMb) {
        super(IronTanksBlockEntities.CREATIVE_TANK.get(), pos, state, capacityMb);
    }

    @Override
    public FluidStack drain(int maxDrain, FluidAction action) {
        return super.drain(maxDrain, FluidAction.SIMULATE);
    }

    @Override
    public FluidStack drain(FluidStack resource, FluidAction action) {
        return super.drain(resource, FluidAction.SIMULATE);
    }

    @Override
    public boolean canConnectTo(TileTank other, Direction direction) {
        return false;
    }
}
