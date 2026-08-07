
package com.indemnity83.irontanks;

import buildcraft.core.BCCore;
import com.indemnity83.irontanks.common.registry.IronTanksBlockEntities;
import com.indemnity83.irontanks.common.registry.IronTanksBlocks;
import com.indemnity83.irontanks.common.registry.IronTanksItems;

//? if neoforge {
/*import buildcraft.api.capabilities.BCCapabilityRegistration;
import buildcraft.lib.misc.CapUtil;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.ModContainer;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.capabilities.RegisterCapabilitiesEvent;
*///?} else {
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;
//?}

@Mod(IronTanks.MODID)
public final class IronTanks {
    public static final String MODID = "irontanks";

    //? if neoforge {
    /*public IronTanks(IEventBus modBus, ModContainer modContainer) {
        init(modBus);
        modBus.addListener(this::registerCapabilities);
    }
    *///?} else {
    public IronTanks() {
        init(FMLJavaModLoadingContext.get().getModEventBus());
    }
    //?}

    private static void init(IEventBus modBus) {
        IronTanksBlocks.register(modBus);
        IronTanksItems.register(modBus);
        IronTanksBlockEntities.register(modBus);
        BCCore.BUILDCRAFT_TAB.addItemProvider(IronTanksItems::getCreativeTabItems);
    }

    //? if neoforge {
    /*private void registerCapabilities(RegisterCapabilitiesEvent event) {
        BCCapabilityRegistration.registerBlockEntity(event, CapUtil.CAP_FLUIDS, IronTanksBlockEntities.TANK.get());
        BCCapabilityRegistration.registerBlockEntity(event, CapUtil.CAP_FLUIDS, IronTanksBlockEntities.CREATIVE_TANK.get());
        BCCapabilityRegistration.registerBlockEntity(event, CapUtil.CAP_FLUIDS, IronTanksBlockEntities.VOID_TANK.get());
    }
    *///?}
}
