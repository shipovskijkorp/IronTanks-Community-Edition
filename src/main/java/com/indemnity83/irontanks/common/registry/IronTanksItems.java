
package com.indemnity83.irontanks.common.registry;

import buildcraft.factory.BCFactoryBlocks;
import com.indemnity83.irontanks.IronTanks;
import com.indemnity83.irontanks.common.item.UpgradeItem;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
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

public final class IronTanksItems {
    //? if neoforge {
    /*public static final DeferredRegister<Item> ITEMS = DeferredRegister.create(Registries.ITEM, IronTanks.MODID);
    *///?} else {
    public static final DeferredRegister<Item> ITEMS = DeferredRegister.create(ForgeRegistries.ITEMS, IronTanks.MODID);
    //?}

    public static final Supplier<BlockItem> COPPER_TANK = blockItem("copper_tank", IronTanksBlocks.COPPER_TANK);
    public static final Supplier<BlockItem> IRON_TANK = blockItem("iron_tank", IronTanksBlocks.IRON_TANK);
    public static final Supplier<BlockItem> SILVER_TANK = blockItem("silver_tank", IronTanksBlocks.SILVER_TANK);
    public static final Supplier<BlockItem> GOLD_TANK = blockItem("gold_tank", IronTanksBlocks.GOLD_TANK);
    public static final Supplier<BlockItem> DIAMOND_TANK = blockItem("diamond_tank", IronTanksBlocks.DIAMOND_TANK);
    public static final Supplier<BlockItem> OBSIDIAN_TANK = blockItem("obsidian_tank", IronTanksBlocks.OBSIDIAN_TANK);
    public static final Supplier<BlockItem> EMERALD_TANK = blockItem("emerald_tank", IronTanksBlocks.EMERALD_TANK);
    public static final Supplier<BlockItem> ALUMINIUM_TANK = blockItem("aluminium_tank", IronTanksBlocks.ALUMINIUM_TANK);
    public static final Supplier<BlockItem> STAINLESSSTEEL_TANK = blockItem("stainlesssteel_tank", IronTanksBlocks.STAINLESSSTEEL_TANK);
    public static final Supplier<BlockItem> TITANIUM_TANK = blockItem("titanium_tank", IronTanksBlocks.TITANIUM_TANK);
    public static final Supplier<BlockItem> TUNGSTENSTEEL_TANK = blockItem("tungstensteel_tank", IronTanksBlocks.TUNGSTENSTEEL_TANK);
    public static final Supplier<BlockItem> VOID_TANK = blockItem("void_tank", IronTanksBlocks.VOID_TANK);
    public static final Supplier<BlockItem> CREATIVE_TANK = blockItem("creative_tank", IronTanksBlocks.CREATIVE_TANK);

    public static final Supplier<UpgradeItem> COPPER_IRON_UPGRADE = upgrade("copper_iron_upgrade", IronTanksBlocks.COPPER_TANK, IronTanksBlocks.IRON_TANK);
    public static final Supplier<UpgradeItem> COPPER_SILVER_UPGRADE = upgrade("copper_silver_upgrade", IronTanksBlocks.COPPER_TANK, IronTanksBlocks.SILVER_TANK);
    public static final Supplier<UpgradeItem> DIAMOND_OBSIDIAN_UPGRADE = upgrade("diamond_obsidian_upgrade", IronTanksBlocks.DIAMOND_TANK, IronTanksBlocks.OBSIDIAN_TANK);
    public static final Supplier<UpgradeItem> GLASS_COPPER_UPGRADE = upgrade("glass_copper_upgrade", BCFactoryBlocks.TANK_BLOCK, IronTanksBlocks.COPPER_TANK);
    public static final Supplier<UpgradeItem> GLASS_IRON_UPGRADE = upgrade("glass_iron_upgrade", BCFactoryBlocks.TANK_BLOCK, IronTanksBlocks.IRON_TANK);
    public static final Supplier<UpgradeItem> GOLD_DIAMOND_UPGRADE = upgrade("gold_diamond_upgrade", IronTanksBlocks.GOLD_TANK, IronTanksBlocks.DIAMOND_TANK);
    public static final Supplier<UpgradeItem> IRON_GOLD_UPGRADE = upgrade("iron_gold_upgrade", IronTanksBlocks.IRON_TANK, IronTanksBlocks.GOLD_TANK);
    public static final Supplier<UpgradeItem> SILVER_GOLD_UPGRADE = upgrade("silver_gold_upgrade", IronTanksBlocks.SILVER_TANK, IronTanksBlocks.GOLD_TANK);
    public static final Supplier<UpgradeItem> DIAMOND_EMERALD_UPGRADE = upgrade("diamond_emerald_upgrade", IronTanksBlocks.DIAMOND_TANK, IronTanksBlocks.EMERALD_TANK);
    public static final Supplier<UpgradeItem> DIAMOND_ALUMINIUM_UPGRADE = upgrade("diamond_aluminium_upgrade", IronTanksBlocks.DIAMOND_TANK, IronTanksBlocks.ALUMINIUM_TANK);
    public static final Supplier<UpgradeItem> EMERALD_STAINLESSSTEEL_UPGRADE = upgrade("emerald_stainlesssteel_upgrade", IronTanksBlocks.EMERALD_TANK, IronTanksBlocks.STAINLESSSTEEL_TANK);
    public static final Supplier<UpgradeItem> ALUMINIUM_STAINLESSSTEEL_UPGRADE = upgrade("aluminium_stainlesssteel_upgrade", IronTanksBlocks.ALUMINIUM_TANK, IronTanksBlocks.STAINLESSSTEEL_TANK);
    public static final Supplier<UpgradeItem> STAINLESSSTEEL_TITANIUM_UPGRADE = upgrade("stainlesssteel_titanium_upgrade", IronTanksBlocks.STAINLESSSTEEL_TANK, IronTanksBlocks.TITANIUM_TANK);
    public static final Supplier<UpgradeItem> TITANIUM_TUNGSTENSTEEL_UPGRADE = upgrade("titanium_tungstensteel_upgrade", IronTanksBlocks.TITANIUM_TANK, IronTanksBlocks.TUNGSTENSTEEL_TANK);

    private static final List<Supplier<? extends Item>> CREATIVE_ITEMS = List.of(
            COPPER_TANK, IRON_TANK, SILVER_TANK, GOLD_TANK, DIAMOND_TANK, OBSIDIAN_TANK,
            EMERALD_TANK, ALUMINIUM_TANK, STAINLESSSTEEL_TANK, TITANIUM_TANK, TUNGSTENSTEEL_TANK,
            VOID_TANK, CREATIVE_TANK,
            GLASS_COPPER_UPGRADE, GLASS_IRON_UPGRADE, COPPER_IRON_UPGRADE, COPPER_SILVER_UPGRADE,
            IRON_GOLD_UPGRADE, SILVER_GOLD_UPGRADE, GOLD_DIAMOND_UPGRADE,
            DIAMOND_OBSIDIAN_UPGRADE, DIAMOND_EMERALD_UPGRADE, DIAMOND_ALUMINIUM_UPGRADE,
            EMERALD_STAINLESSSTEEL_UPGRADE, ALUMINIUM_STAINLESSSTEEL_UPGRADE,
            STAINLESSSTEEL_TITANIUM_UPGRADE, TITANIUM_TUNGSTENSTEEL_UPGRADE
    );

    private IronTanksItems() {
    }

    private static Supplier<BlockItem> blockItem(String name, Supplier<? extends Block> block) {
        return ITEMS.register(name, () -> new BlockItem(block.get(), new Item.Properties()));
    }

    private static Supplier<UpgradeItem> upgrade(String name, Supplier<? extends Block> from, Supplier<? extends Block> to) {
        return ITEMS.register(name, () -> new UpgradeItem(new Item.Properties(), from, to));
    }

    public static List<ItemStack> getCreativeTabItems() {
        return CREATIVE_ITEMS.stream().map(Supplier::get).map(ItemStack::new).toList();
    }

    public static void register(IEventBus bus) {
        ITEMS.register(bus);
    }
}
