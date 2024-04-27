void buildingDestroyed(int buildingIdx = 0, int genIdx = 0) {
    // Set building state to destroyed (false)
    int buildingStates = xsArrayGetInt(BUILDINGS_ALIVE_STATE_ARRAYS, buildingIdx);
    int buildingStateSize = xsArrayGetSize(buildingStates);
    xsArraySetBool(buildingStates, genIdx, false);

    // Decrease alive building count
    int newSize = xsArrayGetInt(BUILDING_COUNTS, buildingIdx) - 1;
    xsArraySetInt(BUILDING_COUNTS, buildingIdx, newSize);

    int temp = xsArrayCreateInt(newSize, 0, "RemainingBuildings_201956843" + buildingIdx + "-" + newSize);

    int insertIndex = 0;
    for (i = 0; < buildingStateSize) {
        if (xsArrayGetBool(buildingStates, i)) {
            xsArraySetInt(temp, insertIndex, i);
            insertIndex++;
        }
    }

    xsArraySetInt(BUILDINGS_ALIVE_IDX_ARRAYS, buildingIdx, temp);
}

void spawnRandomUnit(int buildingIdx = 0, int unitIdx = 0) {
    int temp = xsArrayGetInt(BUILDINGS_ALIVE_IDX_ARRAYS, buildingIdx);
    int size = xsArrayGetSize(temp);
    if (size == 0) { return; }
    
    int genIdxIdx = GetRandomRange(0, size - 1);
    int foundGenIdx = xsArrayGetInt(temp, genIdxIdx);

    // Currently unused!
}

void setUnitSpawnRate(int unitIdx = 0, int rate = 0) {
    if (rate == 0) {
        return;
    }

    // Maximum rate currently: `30`. Due to condition Timer(1) issues
    if (rate > 30) {
        rate = 30;
    }

    // `rate = rate / 60 * 100`
    rate = rate / 0.6;

    xsArraySetInt(UNIT_SPAWN_CHANCE_ARRAY, unitIdx, rate);
}

bool shouldSpawn(int unitIdx = 0) {
    int rate = xsArrayGetInt(UNIT_SPAWN_CHANCE_ARRAY, unitIdx);
    if (rate == 0) {
        return (false);
    }

    int coin = GetRandomRange(0, 99);
    if (coin <= rate) {
        return (true);
    }

    return (false);
}

void decreaseUnitQueue(int unitIdx = 0) {
    int queue = xsArrayGetInt(UNIT_QUEUE_ARRAY, unitIdx);
    xsArraySetInt(UNIT_QUEUE_ARRAY, unitIdx, queue - 1);
}

void increaseUnitQueue(int unitIdx = 0, int amount = 1) {
    int queue = xsArrayGetInt(UNIT_QUEUE_ARRAY, unitIdx);
    xsArraySetInt(UNIT_QUEUE_ARRAY, unitIdx, queue + amount);
}

bool trainUnitCondition(int unitIdx = 0) {
    int queue = xsArrayGetInt(UNIT_QUEUE_ARRAY, unitIdx);

    if (queue > 0) {
        decreaseUnitQueue(unitIdx);
        return (true);
    }

    return (false);
}