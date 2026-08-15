package com.indemnity83.irontanks.common.guide;

import buildcraft.api.v2.content.BuildCraftContent;
import buildcraft.api.v2.content.ContentRegistrar;
import buildcraft.api.v2.guide.GuideEntry;
import buildcraft.api.v2.guide.GuidePages;
import buildcraft.api.v2.guide.GuideSection;
import com.indemnity83.irontanks.IronTanks;
import net.minecraft.resources.ResourceLocation;

/** Registers Iron Tanks documentation through BuildCraft Extension API 2. */
public final class IronTanksGuide {
    private static final String[] TANKS = {
        "copper_tank", "iron_tank", "silver_tank", "gold_tank", "diamond_tank",
        "obsidian_tank", "emerald_tank", "aluminium_tank", "stainlesssteel_tank",
        "titanium_tank", "tungstensteel_tank", "void_tank", "creative_tank"
    };

    private static final String[] UPGRADES = {
        "glass_copper_upgrade", "glass_iron_upgrade", "copper_iron_upgrade", "copper_silver_upgrade",
        "iron_gold_upgrade", "silver_gold_upgrade", "gold_diamond_upgrade", "diamond_obsidian_upgrade",
        "diamond_emerald_upgrade", "diamond_aluminium_upgrade", "emerald_stainlesssteel_upgrade",
        "aluminium_stainlesssteel_upgrade", "stainlesssteel_titanium_upgrade", "titanium_tungstensteel_upgrade"
    };

    private IronTanksGuide() {
    }

    public static void register() {
        ContentRegistrar content = BuildCraftContent.addon(IronTanks.MODID);
        ResourceLocation root = content.id("guide");
        ResourceLocation tanks = content.id("guide/tanks");
        ResourceLocation upgrades = content.id("guide/upgrades");

        content.guideSection(GuideSection.builder(root, "irontanks.guide.section.root")
            .icon(content.id("iron_tank"))
            .order(300)
            .build());
        content.guideSection(GuideSection.builder(tanks, "irontanks.guide.section.tanks")
            .parent(root)
            .icon(content.id("iron_tank"))
            .order(0)
            .build());
        content.guideSection(GuideSection.builder(upgrades, "irontanks.guide.section.upgrades")
            .parent(root)
            .icon(content.id("iron_gold_upgrade"))
            .order(100)
            .build());

        registerEntries(content, tanks, TANKS, true);
        registerEntries(content, upgrades, UPGRADES, false);
    }

    private static void registerEntries(ContentRegistrar content, ResourceLocation section, String[] names, boolean blocks) {
        for (int index = 0; index < names.length; index++) {
            String name = names[index];
            ResourceLocation itemId = content.id(name);
            String titleKey = (blocks ? "block." : "item.") + IronTanks.MODID + "." + name;
            String guideKey = "irontanks.guide." + name;
            content.guideEntry(GuideEntry.builder(content.id("guide/" + name), section, titleKey)
                .icon(itemId)
                .order(index * 10)
                .page(GuidePages.textKey(guideKey + ".intro"))
                .page(GuidePages.item(itemId, guideKey + ".details"))
                .build());
        }
    }
}
