int playerPositions = 0;
bool playerShuffleFinished = false;

void ShuffleIntArray(int arr = -1) {
    if (arr == -1)
        return;
    
    int n = xsArrayGetSize(arr);
    for (i = 0; < n) {
        int j = GetRandomRange(0, n - 1);
        int v = xsArrayGetInt(arr, j);
        xsArraySetInt(arr, j, xsArrayGetInt(arr, i));
        xsArraySetInt(arr, i, v);
    }
}

rule randomize_player_spawns__654825569
    active
    runImmediately
    minInterval 1
    maxInterval 1
    priority 999
{
    playerPositions = xsArrayCreateInt(7, 0, "__player_positions_458752359");

    for(i = 0; < 7) {
        xsArraySetInt(playerPositions, i, i);
    }

    ShuffleIntArray(playerPositions);

    playerShuffleFinished = true;

    xsDisableSelf();
}