package com.indemnity83.irontanks;

import buildcraft.core.BCCore;
import com.indemnity83.irontanks.common.guide.IronTanksGuide;
import com.indemnity83.irontanks.common.registry.IronTanksBlockEntities;
import com.indemnity83.irontanks.common.registry.IronTanksBlocks;
import com.indemnity83.irontanks.common.registry.IronTanksItems;

import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.ModContainer;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.capabilities.RegisterCapabilitiesEvent;

@Mod(IronTanks.MODID)
public final class IronTanks {
    public static final String MODID = "irontanks";

    public IronTanks(IEventBus modBus, ModContainer modContainer) {
        init(modBus);
        modBus.addListener(this::registerCapabilities);
    }

    private static void init(IEventBus modBus) {
        IronTanksBlocks.register(modBus);
        IronTanksItems.register(modBus);
        IronTanksBlockEntities.register(modBus);
        BCCore.BUILDCRAFT_TAB.addItemProvider(IronTanksItems::getCreativeTabItems);

        // API2 registration is code-owned and must happen before BuildCraft freezes addon content.
        IronTanksGuide.register();
    }

    private void registerCapabilities(RegisterCapabilitiesEvent event) {
        // NeoForge capabilities belong to the loader, not BuildCraft's internal capability helpers.
        // BuildCraft API2 discovers these native handlers through its platform fluid bridge.
        event.registerBlockEntity(Capabilities.FluidHandler.BLOCK, IronTanksBlockEntities.TANK.get(), (tank, side) -> tank);
        event.registerBlockEntity(Capabilities.FluidHandler.BLOCK, IronTanksBlockEntities.CREATIVE_TANK.get(), (tank, side) -> tank);
        event.registerBlockEntity(Capabilities.FluidHandler.BLOCK, IronTanksBlockEntities.VOID_TANK.get(), (tank, side) -> tank);
    }
}
