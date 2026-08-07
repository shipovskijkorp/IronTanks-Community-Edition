
package com.indemnity83.irontanks.common.registry;

import com.indemnity83.irontanks.IronTanks;
import com.indemnity83.irontanks.common.block.CreativeTankBlock;
import com.indemnity83.irontanks.common.block.StackableTankBlock;
import com.indemnity83.irontanks.common.block.TankBlock;
import com.indemnity83.irontanks.common.block.VoidTankBlock;
import net.minecraft.world.level.block.Block;

//? if neoforge {
/*import net.minecraft.core.registries.Registries;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredRegister;
*///?} else {
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
//?}

import java.util.List;
import java.util.function.Supplier;

public final class IronTanksBlocks {
    //? if neoforge {
    /*public static final DeferredRegister<Block> BLOCKS = DeferredRegister.create(Registries.BLOCK, IronTanks.MODID);
    *///?} else {
    public static final DeferredRegister<Block> BLOCKS = DeferredRegister.create(ForgeRegistries.BLOCKS, IronTanks.MODID);
    //?}

    public static final Supplier<StackableTankBlock> COPPER_TANK = BLOCKS.register("copper_tank", () -> new StackableTankBlock(27, 4.0F, 2.0F));
    public static final Supplier<StackableTankBlock> IRON_TANK = BLOCKS.register("iron_tank", () -> new StackableTankBlock(32, 5.0F, 3.0F));
    public static final Supplier<StackableTankBlock> SILVER_TANK = BLOCKS.register("silver_tank", () -> new StackableTankBlock(43, 6.0F, 5.0F));
    public static final Supplier<StackableTankBlock> GOLD_TANK = BLOCKS.register("gold_tank", () -> new StackableTankBlock(48, 7.0F, 4.0F));
    public static final Supplier<StackableTankBlock> DIAMOND_TANK = BLOCKS.register("diamond_tank", () -> new StackableTankBlock(64, 8.0F, 6.0F));
    public static final Supplier<StackableTankBlock> OBSIDIAN_TANK = BLOCKS.register("obsidian_tank", () -> new StackableTankBlock(64, 50.0F, 1_200.0F));
    public static final Supplier<StackableTankBlock> EMERALD_TANK = BLOCKS.register("emerald_tank", () -> new StackableTankBlock(96, 8.0F, 6.0F));
    public static final Supplier<StackableTankBlock> ALUMINIUM_TANK = BLOCKS.register("aluminium_tank", () -> new StackableTankBlock(96, 5.0F, 4.0F));
    public static final Supplier<StackableTankBlock> STAINLESSSTEEL_TANK = BLOCKS.register("stainlesssteel_tank", () -> new StackableTankBlock(128, 9.0F, 8.0F));
    public static final Supplier<StackableTankBlock> TITANIUM_TANK = BLOCKS.register("titanium_tank", () -> new StackableTankBlock(256, 10.0F, 10.0F));
    public static final Supplier<StackableTankBlock> TUNGSTENSTEEL_TANK = BLOCKS.register("tungstensteel_tank", () -> new StackableTankBlock(512, 12.0F, 14.0F));
    public static final Supplier<VoidTankBlock> VOID_TANK = BLOCKS.register("void_tank", () -> new VoidTankBlock(8, 5.0F, 6.0F));
    public static final Supplier<CreativeTankBlock> CREATIVE_TANK = BLOCKS.register("creative_tank", () -> new CreativeTankBlock(1));

    public static final List<Supplier<? extends TankBlock>> NORMAL_TANKS = List.of(
            COPPER_TANK, IRON_TANK, SILVER_TANK, GOLD_TANK, DIAMOND_TANK, OBSIDIAN_TANK,
            EMERALD_TANK, ALUMINIUM_TANK, STAINLESSSTEEL_TANK, TITANIUM_TANK, TUNGSTENSTEEL_TANK
    );

    public static final List<Supplier<? extends TankBlock>> ALL_TANKS = List.of(
            COPPER_TANK, IRON_TANK, SILVER_TANK, GOLD_TANK, DIAMOND_TANK, OBSIDIAN_TANK,
            EMERALD_TANK, ALUMINIUM_TANK, STAINLESSSTEEL_TANK, TITANIUM_TANK, TUNGSTENSTEEL_TANK,
            VOID_TANK, CREATIVE_TANK
    );

    private IronTanksBlocks() {
    }

    public static void register(IEventBus bus) {
        BLOCKS.register(bus);
    }
}
