
package com.indemnity83.irontanks.common.blockentity;

import buildcraft.factory.tile.TileTank;
import com.indemnity83.irontanks.common.block.TankBlock;
import com.indemnity83.irontanks.common.registry.IronTanksBlockEntities;
import net.minecraft.core.BlockPos;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;

public class TankTile extends TileTank {
    private static final int FALLBACK_CAPACITY = 16_000;

    public TankTile(BlockPos pos, BlockState state) {
        this(IronTanksBlockEntities.TANK.get(), pos, state, capacityFromState(state));
    }

    public TankTile(BlockPos pos, BlockState state, int capacityMb) {
        this(IronTanksBlockEntities.TANK.get(), pos, state, capacityMb);
    }

    protected TankTile(BlockEntityType<?> type, BlockPos pos, BlockState state, int capacityMb) {
        super(type, capacityMb, pos, state);
    }

    protected static int capacityFromState(BlockState state) {
        if (state.getBlock() instanceof TankBlock tankBlock) {
            return tankBlock.getCapacityMb();
        }
        return FALLBACK_CAPACITY;
    }
}
