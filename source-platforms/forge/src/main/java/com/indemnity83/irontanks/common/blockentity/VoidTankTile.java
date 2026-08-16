
package com.indemnity83.irontanks.common.blockentity;

import com.indemnity83.irontanks.common.registry.IronTanksBlockEntities;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.block.state.BlockState;

import net.minecraftforge.fluids.capability.IFluidHandler.FluidAction;

public final class VoidTankTile extends TankTile {
    * Matches the default BuildCraft CE void fluid pipe rate: base fluid rate 10 * 8.
    private static final int TRANSFER_PER_TICK = 80;

    public VoidTankTile(BlockPos pos, BlockState state) {
        this(pos, state, capacityFromState(state));
    }

    public VoidTankTile(BlockPos pos, BlockState state, int capacityMb) {
        super(IronTanksBlockEntities.VOID_TANK.get(), pos, state, capacityMb);
    }

    @Override
    public void update() {
        super.update();
        if (level == null || level.isClientSide) {
            return;
        }

        int amount = tank.getFluidAmount();
        if (amount > 0) {
            tank.drainInternal(Math.min(amount, TRANSFER_PER_TICK), FluidAction.EXECUTE);
        }
    }
}
