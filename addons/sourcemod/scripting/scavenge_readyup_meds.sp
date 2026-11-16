#pragma semicolon 1
#pragma newdecls required

#include <sourcemod>
#include <sdkhooks>
#include <left4dhooks>
#undef REQUIRE_PLUGIN
#include <readyup>
#define REQUIRE_PLUGIN

public Plugin myinfo =
{
    name        = "Scavenge ReadyUp Meds",
    author      = "lechuga",
    description = "Blocks pills and adrenaline pickup during Scavenge ready-up.",
    version     = "1.0.0",
    url         = "https://github.com/AoC-Gamers/Scavogl-Rework"
};

enum struct PluginRuntimeState
{
    bool lateLoad;
    bool hasReadyUp;
}

PluginRuntimeState g_Runtime;
ConVar             g_cvEnabled;
ConVar             g_cvDebug;

public APLRes AskPluginLoad2(Handle myself, bool late, char[] error, int errMax)
{
    g_Runtime.lateLoad = late;
    return APLRes_Success;
}

public void OnPluginStart()
{
    L4D2_InitWeaponNameTrie();

    g_cvEnabled = CreateConVar("sm_scavenge_readyup_meds_enable", "1", "Block pills and adrenaline pickup during Scavenge ready-up.", FCVAR_NOTIFY, true, 0.0, true, 1.0);
    g_cvDebug   = CreateConVar("sm_scavenge_readyup_meds_debug", "0", "Print medical WeaponCanUse diagnostics to server console.", FCVAR_NONE, true, 0.0, true, 1.0);

    if (!g_Runtime.lateLoad)
        return;

    for (int client = 1; client <= MaxClients; client++)
    {
        if (!IsClientInGame(client))
            continue;

        OnClientPutInServer(client);
    }
}

public void OnAllPluginsLoaded()
{
    g_Runtime.hasReadyUp = LibraryExists("readyup");
    if (g_Runtime.hasReadyUp)
        return;

    PrintToServer("[Scavenge ReadyUp Meds] ReadyUp unavailable; medical pickup protection is inactive.");
}

public void OnLibraryAdded(const char[] name)
{
    if (!StrEqual(name, "readyup"))
        return;

    g_Runtime.hasReadyUp = true;
}

public void OnLibraryRemoved(const char[] name)
{
    if (!g_Runtime.hasReadyUp || !StrEqual(name, "readyup"))
        return;

    g_Runtime.hasReadyUp = false;
    PrintToServer("[Scavenge ReadyUp Meds] ReadyUp removed; medical pickup protection is inactive.");
}

public void OnClientPutInServer(int client)
{
    SDKHook(client, SDKHook_WeaponCanUse, OnWeaponCanUse);
}

public void OnClientDisconnect(int client)
{
    SDKUnhook(client, SDKHook_WeaponCanUse, OnWeaponCanUse);
}

public void OnPluginEnd()
{
    for (int client = 1; client <= MaxClients; client++)
    {
        if (!IsClientInGame(client))
            continue;

        SDKUnhook(client, SDKHook_WeaponCanUse, OnWeaponCanUse);
    }
}

public Action OnWeaponCanUse(int client, int weapon)
{
    if (!g_cvEnabled.BoolValue || !g_Runtime.hasReadyUp || !L4D2_IsScavengeMode() || !IsInReady())
        return Plugin_Continue;

    if (client < 1 || client > MaxClients || !IsClientInGame(client)
        || L4D_GetClientTeam(client) != L4DTeam_Survivor || weapon <= MaxClients || !IsValidEntity(weapon))
        return Plugin_Continue;

    L4D2WeaponId weaponId = L4D2_GetWeaponId(weapon);

    if (weaponId != L4D2WeaponId_PainPills && weaponId != L4D2WeaponId_Adrenaline)
        return Plugin_Continue;

    PrintDebug(client, weapon);

    return Plugin_Handled;
}

void PrintDebug(int client, int weapon)
{
    if (!g_cvDebug.BoolValue)
        return;

    char classname[64];
    GetEntityClassname(weapon, classname, sizeof(classname));
    PrintToServer("[Scavenge ReadyUp Meds] client=%d bot=%d entity=%d classname=%s",
                  client, IsFakeClient(client), weapon, classname);
}
