
package com.indemnity83.irontanks.common.registry;

import com.indemnity83.irontanks.IronTanks;
import com.indemnity83.irontanks.common.blockentity.CreativeTankTile;
import com.indemnity83.irontanks.common.blockentity.TankTile;
import com.indemnity83.irontanks.common.blockentity.VoidTankTile;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.entity.BlockEntityType;

import net.minecraft.core.registries.Registries;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredRegister;

import java.util.function.Supplier;

public final class IronTanksBlockEntities {
    public static final DeferredRegister<BlockEntityType<?>> BLOCK_ENTITIES = DeferredRegister.create(Registries.BLOCK_ENTITY_TYPE, IronTanks.MODID);

    public static final Supplier<BlockEntityType<TankTile>> TANK = BLOCK_ENTITIES.register("tank", () ->
            BlockEntityType.Builder.of(TankTile::new, normalTankBlocks()).build(null));

    public static final Supplier<BlockEntityType<CreativeTankTile>> CREATIVE_TANK = BLOCK_ENTITIES.register("creative_tank", () ->
            BlockEntityType.Builder.of(CreativeTankTile::new, IronTanksBlocks.CREATIVE_TANK.get()).build(null));

    public static final Supplier<BlockEntityType<VoidTankTile>> VOID_TANK = BLOCK_ENTITIES.register("void_tank", () ->
            BlockEntityType.Builder.of(VoidTankTile::new, IronTanksBlocks.VOID_TANK.get()).build(null));

    private IronTanksBlockEntities() {
    }

    private static Block[] normalTankBlocks() {
        return IronTanksBlocks.NORMAL_TANKS.stream().map(Supplier::get).toArray(Block[]::new);
    }

    public static void register(IEventBus bus) {
        BLOCK_ENTITIES.register(bus);
    }
}
