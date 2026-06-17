// dllmain.cpp : 定义 DLL 应用程序的入口点。
#include "pch.h"
#include "naclo_image1.h"
BOOL APIENTRY DllMain( HMODULE hModule,
                       DWORD  ul_reason_for_call,
                       LPVOID lpReserved
                     )
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}
#define EXPORT extern "C" __declspec(dllexport)
EXPORT
bool CropImage(const char* src,const char* dst,int x,int y,int w,int h)
{
    NaClO_ImageResult T = NaClO_Load(src);
    if (T.Error != NACLO_OK)
    {
        return false;
    }

    NaClO_ImageResult T2 = NaClO_Crop(&T.result, x, y, w, h);
    NaClO_FreeImage(&T.result);
    
    auto result=NaClO_SaveAndFree(&T2.result, dst);
    return result == NACLO_OK;
}

