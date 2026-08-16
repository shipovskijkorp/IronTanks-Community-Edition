package com.indemnity83.irontanks;

import buildcraft.core.BCCore;
import com.indemnity83.irontanks.common.guide.IronTanksGuide;
import com.indemnity83.irontanks.common.registry.IronTanksBlockEntities;
import com.indemnity83.irontanks.common.registry.IronTanksBlocks;
import com.indemnity83.irontanks.common.registry.IronTanksItems;

import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;

@Mod(IronTanks.MODID)
public final class IronTanks {
    public static final String MODID = "irontanks";

    public IronTanks() {
        init(FMLJavaModLoadingContext.get().getModEventBus());
    }

    private static void init(IEventBus modBus) {
        IronTanksBlocks.register(modBus);
        IronTanksItems.register(modBus);
        IronTanksBlockEntities.register(modBus);
        BCCore.BUILDCRAFT_TAB.addItemProvider(IronTanksItems::getCreativeTabItems);

        // API2 registration is code-owned and must happen before BuildCraft freezes addon content.
        IronTanksGuide.register();
    }

}
