# DefendTheMonument

## Gameplay

It's a 7v1 against the AI player. There's a monument in the center which needs to be defended.

---

**To be fair, even the lose-condition (the monument) could be changed if a better alternative is found**

---

### 1. Player

1. Should players start with a TC?
   1. **NO** 
      1. No starting tc would make the play-through a lot more dynamic
         1. What distance should people be incentivized to place their starting TCs to the center monument
            1. Close like before? 
            2. Little more space (~15 tiles all directions), so it doesn't become a clusterfuck (like before 11)
            3. Anywhere (True nomad start?)
      2. It'd require balancing all civs for their starting bonuses (cannot be done automatically like nomad) 
         1. Would require updating the map once balance changes come in that affect it
   2. **YES**
      1. No issues with starting resources per civ
         1. No balance changes needed to the map when civ balance happens
      2. Super easy for players who've never played before (so people might continue playing more often)
         1. ~~Settings in scenario itself ????~~ ::: **Definitely eventually, but will take too much time for v0.1**
   3. **FOUNDATION ONLY** 
      1. More noob friendly (noob as in 'first' time scenario players)
      2. Potentially (didn't look into it) solves (a part of) the starting resource problem **_(???)_**
      3. Deletable for dynamic placements

### 2. Resources

1. Dynamic or static resources (gold/stone/berries/boars/deer etc.)? 
   1. If dynamic, need to test it with 8 players more. Make sure no crashes occur. 
2. Should I try dynamic forests? That's an insane amount of triggers. 
   1. Maybe don't do forests _as dynamic_ as other resources and make it choose between `n` different formations?
      1. This'd be only `n` trigger spawning hundreds of trees on designated locations
      2. Can make sure all areas are covered with 'tree terrain', so they're not seen as stragglers
   2. Random forests might cause more effort with random vill spawning if working with nomad start **_(???)_**

### 3. Enemy

1. Should the enemy have (useful) eco?
   1. Should it be functional eco, or artificial?
      1. Artificial meaning if you kill farmers, the AI gets less free food (cheated in by triggers)
      2. If functional eco, how many vills or increase work rate?
   2. ~~AI needs to be relatively advanced for functional ECO to balance ECO based on units~~. ::: **Simply too much work**.
2. Should the enemy receive units for free, ~~or resources (using eco, see above)~~ ::: **Simply too much work**
   1. ~~If resources for free, an advanced (civ based) AI needs to be written~~ ::: **Simply too much work**
   2. Receiving units through triggers
      1. A LOT easier to control (without learning AI scripting) 
      2. Also allows the use of units (& techs) the CIV doesn't have access too
      3. Also allows for the use of units and techs of multiple civs at once (Maybe not? See header **3.** below)
      4. Should there be a way to impact what is spawned?
         1. Have gen buildings around the map, kill a barracks and less infantry spawns?
         2. Actually use the gen buildings with `Train Unit` effect?
3. Should civilization impact the units/upgrades of the AI?
   1. Not too difficult to program with triggers, though balancing is a bit more work
      1. Properly balancing could take A LOT of work. But maybe it's good to have built-in difficulty through civs?
   2. This'd probably impact other unit balance too.
      1. E.g. hindustanis should not just have no KTS but also have more camels than other camel civs
4. Should the enemy scale based on the amount of players (incl. friendly AI (?))
   1. What should be affected? Time or just spawn numbers
      1. ~~Proper non-linear balance~~ ::: **For a later version, a lot of work**
      2. Scale linearly (Relatively simple with XS (I think)) `units_spawned = units_per_minute * players`
         1. In the spot that spawns a unit/resource (use a `for _ in range(len(players))` (XS version))

### 4. Lose-condition

1. How do you lose the monument?
   1. **CONVERSION** (like before)
      1. Was quite confusing for players. The moment no units are around and an enemy was close, you lost instantly
   2. **DAMAGE** (When monument is broken you lose)
      1. **INDIRECTLY** Any unit that gets too close will be removed and the monument will receive `x` amount of damage
      2. **DIRECTLY** Change the AI, so it targets the monument directly sometimes
         1. Can potentially copy the AI used in magundai madness
2. All / Any players die?
   1. Probably not, but *could* be an option. Probably not good for MP

### 5. Win-condition

1. How do you win the scenario?
   1. **You don't** --- Hold out as long as you can
      1. Not liked as much by players (especially since no leaderboard)
      2. Keep increasing difficulty by adding more upgrades/units over time (automatically)
   2. **A certain amount of time**
      1. Try and survive for an X amount of time, and you win (i.e. in-game hour (?))
      2. Might cause more defensive play
      3. Allow to continue after you won? (If you lose monument after, still give victory to players?) 
   3. **Objectives**
      1. **Obtain X** --- (i.e. "Obtain all relics")
         1. Find something across the entire map and bring it to the center (?) and win
         2. Could be cheesed? I.e. Distract units and speed run the win, might not be 'fun'
      2. **KILL the AI**
         1. Kill stuff of the AI. Incentivizes more aggressive play 
            1. If it has economy, kill until no more units spawn
               1. Raiding enemy eco could become a thing. Is that a good thing?
            2. If it has gen buildings, kill all that so no more units can spawn
               1. Could result in trebuchet spam. Is that a bad thing?
               2. Doesn't matter if gen buildings used directly or indirectly (See header **3. Enemy 2.4**)
   4. **Achievement**
      1. **Kill X units**
         1. Basically the same as defence, but might be a little more interesting compared to waiting for a timer

---

### 1. Player

No TC or foundation @ start with a little more space than before
No balancing of civs needed for now, probably needed in future

Fortified Palisades to Feudal (???)
Stone walls > Castle age
Fortified walls > Imp (if not already)

### 2. Resources

Preferably random if no crashes occur.
If too heavy, spawn resources in separate cycles (?)

Forests, not dynamic (For now)

### 3. Enemy

AI does NOT have useful ECO
AI does use gen buildings (Train Unit effect) surround with castles & towers etc.
AI has small outposts with couple buildings around the map to slow expand
Outposts might contain monastery with multiple relics

For later:
  - Unit that can build unique buildings which provide passive bonuses?

Keep track of what gen buildings are not destroyed and select random one to spawn unit

Random walled in towers around the map to make expanding harder?

Researches can be executed in the buildings they belong in using `Research tech effect`
!! Age can be cheated as exception !!

In IMP: If feudal age upgrade doesn't queue after being queued, disable that unit
(Automatically disable civs that have access to only feudal units)
Could also be hardcoded as there are very few.

Dynamically increase siege if `pop > x` [Petards & Saboteurs & Siege]
Scale AI resources with amount of units if `pop > y`

Scale AI unit spawn with amount of players linearly

For later:
  - Balance resource income based on civ & age
  - At the end of every minute, try and spend all remaining resources
    - Maybe set to average of all 3 resources first

### 4. Lose-condition

Direct damage to monument by AI

### 5. Win-condition

Multiple win conditions would be nice. 
- Time is 'worst' win condition
- Points (to 50?) ? (Based on difficulty?)
  - Kill a gen building = +2
  - Kill a castle       = +5
  - Acquire a relic     = +1

# Ideas

- Split the spawn areas in chunks and fortify to force units from all angles
- [REQUIRED DATAMOD] Units from Dark Age with focus walls over units (like rams)?
- Petard with less blast damage in Dark Age
- Instantly delete all p8 buildings in center (delete converted buildings)
  - Maybe filter potential buildings p8 might eventually get in map generation?
