
package com.indemnity83.irontanks.common.block;

import buildcraft.factory.block.ITankBlockConnector;

public class StackableTankBlock extends TankBlock implements ITankBlockConnector {
    public StackableTankBlock(int capacityBuckets, float hardness, float resistance) {
        super(capacityBuckets, hardness, resistance);
    }
}
