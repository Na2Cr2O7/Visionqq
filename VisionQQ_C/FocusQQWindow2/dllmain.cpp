// dllmain.cpp : 定义 DLL 应用程序的入口点。
#include "pch.h"

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
bool fileExists(const wchar_t* fileName);
//bool fileExists2(const wchar_t* fileName);
static bool stringInString(const std::wstring& text, const std::wstring& search);
static BOOL CALLBACK addToListIfIsQQ(HWND hwnd, LPARAM lparam);
const std::wstring QQ = L"QQ";
std::vector<HWND> hwnds;

using namespace inicpp;

extern "C" int __declspec(dllexport) focus(bool alwaysOnTop)
{

    if (not fileExists(L"config.ini"))
    {
        std::cerr << "config.ini not exist\n";
        return -1;
    }

    IniManager ini("config.ini");
    int width = 1280;
    int height = 720;

    //使用dll时要额外获取scale
    float scale = 1.0f;
    try
    {
        width = ini["general"]["width"].get<int>();
        height = ini["general"]["height"].get<int>();
        scale = ini["general"]["scale"].get<float>();

    }
    catch (const std::exception& e)
    {
        std::cerr << e.what() << std::endl;
    }

    width *= scale;
    height *= scale;

    hwnds.reserve(4);

    //auto desktop = GetDesktopWindow();

    EnumWindows(addToListIfIsQQ, NULL);

    for (std::vector<HWND>::iterator phwnd = hwnds.begin(); phwnd < hwnds.end(); ++phwnd)
    {
        //SetWindowPos(*phwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOSIZE);
        //SetWindowPos(*phwnd, HWND_TOPMOST, 0, 0, width,height, SWP_NOMOVE);
        bool success = false;
        if (alwaysOnTop)
        {
           success= SetWindowPos(*phwnd, HWND_TOPMOST, 0, 0, width, height, 0);
        }
        else

        {
            success = SetWindowPos(*phwnd, HWND_NOTOPMOST, 0, 0, width, height, 0);

        }
    
        if (not success)
        {
            continue;
        }
        //RECT rect{};
        //if (GetWindowRect(*phwnd, &rect))
        //{
        //    std::wcout << L"Window 0x" << std::hex << reinterpret_cast<uintptr_t>(*phwnd)
        //        << L": (" << std::dec << rect.left << L"," << rect.top
        //        << L") -> (" << (rect.left + width) << L"," << (rect.top + height) << L")\n";
        //}
        //std::wcout << *phwnd << ":" << rect.left << "," << rect.top << "," << rect.left << "," << rect.right << std::endl;
    }
    return 0;

    /*  std::cout << "Hello World!\n";*/
}
static bool correct(const std::wstring_view& text);

static BOOL CALLBACK addToListIfIsQQ(HWND hwnd, LPARAM lparam)
{
    //wchar_t windowName[MAX_PATH]{};
    if (not IsWindowVisible(hwnd))
    {
        return true;
    }
    int length = GetWindowTextLength(hwnd);
    if (not length) return true;
    std::unique_ptr<wchar_t[]> windowName = std::make_unique<wchar_t[]>(static_cast<size_t>(length) + 1);

    length = GetWindowText(hwnd, windowName.get(), MAX_PATH);
    if (not length) return true;

    //if (stringInString(std::wstring(windowName.get(), length), QQ))
    //{
    //    hwnds.push_back(hwnd);
    //}

    if (correct(std::wstring_view(windowName.get(), length)))
    {
        hwnds.push_back(hwnd);
    }
    return true;
}
static bool stringInString(const std::wstring& text, const std::wstring& search)
{
    return text.find(search) != std::wstring::npos;
}
static bool correct(const std::wstring_view& text)
{
    std::wstring correct2 = L"[#] QQ [#]";
    return (text == correct2 or text == QQ);

}
bool fileExists(const wchar_t* fileName)
{
    wchar_t workingDirectory[MAX_PATH]{};
    GetCurrentDirectory(MAX_PATH, workingDirectory);
    //std::wcout << workingDirectory;
    if (std::wcslen(workingDirectory) > MAX_PATH - 1)
    {
        return false;
    }
    std::wcscat(workingDirectory, L"\\");
    std::wcscat(workingDirectory, fileName);
    DWORD attributes = GetFileAttributes(workingDirectory);
    if (attributes != INVALID_FILE_ATTRIBUTES)
    {
        return !(attributes & FILE_ATTRIBUTE_DIRECTORY);
    }
    return false;
}

