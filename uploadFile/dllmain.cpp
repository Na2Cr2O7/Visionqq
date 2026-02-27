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


std::wstring selectedImage;
static BOOL CALLBACK uploadFile(HWND hwnd, LPARAM lparam);
static bool stringInString(const std::wstring& text, const std::wstring& search)
{
	return text.find(search) != std::wstring::npos;
}
extern "C" int __declspec(dllexport) upload()
{


	const wchar_t* imageExts[] = { L".gif",L".png",L".jpg",L".jpeg",L".webp",L".avif",L".bmp" };
	//列出所有文件
	WIN32_FIND_DATA findFileData;
	
	HANDLE hFind = INVALID_HANDLE_VALUE;
	WCHAR pathwithastar[MAX_PATH];
	WCHAR path[MAX_PATH];

	GetCurrentDirectory(MAX_PATH, pathwithastar);
	std::wcscat(pathwithastar, L"\\Images\\*");
	//std::wcscat(pathwithastar, L"\\Images\\");
	std::wcsncpy(path, pathwithastar, std::wcslen(pathwithastar) - 1);

	std::wcout << pathwithastar << std::endl;
	std::wcout << path << std::endl;
	;
	std::vector<std::wstring> images;

	hFind = FindFirstFile(pathwithastar, &findFileData);
	if (hFind == INVALID_HANDLE_VALUE)
	{
		std::wcerr << "错误:" << GetLastError() << std::endl;
		return -2;

	}
	do {
		if (std::wcscmp(findFileData.cFileName, L"..") == 0)
		{
			continue;
		}
		if (std::wcscmp(findFileData.cFileName, L".") == 0)
		{
			continue;
		}
		//图片文件
		for (int i = 0; i < 6; ++i)
		{
			const wchar_t* ext = imageExts[i];
			size_t length = std::wcslen(ext);
			//std::wcout << ext << length;
			//std::cout << std::endl;
			size_t fileNameLength = std::wcslen(findFileData.cFileName);
			if (std::wcscmp(findFileData.cFileName + fileNameLength + 1 - length, ext) == 0)
			{


				goto Picture;
			}

		}
	Picture:
		//std::wcout << findFileData.cFileName << std::endl;
		images.emplace_back(std::wstring(findFileData.cFileName));
	} while (FindNextFile(hFind, &findFileData));


	for (auto& image : images)
	{
		std::wcout << image << std::endl;
	}
	unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
	std::shuffle(images.begin(), images.end(), std::default_random_engine(seed));
	if (images.size() == 0)
	{
		std::wcerr << TEXT("没有找到图片") << std::endl;
		return -1;
	}
	selectedImage = std::wstring(path, std::wcslen(pathwithastar) - 1) + images.at(0);

	// 上传文件
	EnumWindows(uploadFile, NULL);
	return 0;
}


static BOOL CALLBACK uploadFile(HWND hwnd, LPARAM lparam)
{
	//wchar_t windowName[MAX_PATH]{};
	if (not IsWindowVisible(hwnd))
	{
		return true;
	}
	int length = GetWindowTextLength(hwnd);
	if (not length) return true;
	std::unique_ptr<wchar_t[]> windowName = std::make_unique<wchar_t[]>(static_cast<size_t>(length) + 1);
	int success = GetWindowText(hwnd, windowName.get(), MAX_PATH);
	if (not success)
	{
		return true;
	}
	//return true;
	std::wcout << windowName.get() << std::endl;
	if (stringInString(std::wstring(windowName.get(), length), L"请选择"))
	{

		HWND comboboxEx32 = FindWindowEx(hwnd, NULL, L"ComboBoxEx32", NULL);
		HWND combobox = FindWindowEx(comboboxEx32, NULL, L"ComboBox", NULL);
		HWND edit = FindWindowEx(combobox, NULL, L"Edit", NULL);
		SendMessage(edit, WM_SETTEXT, NULL, (LPARAM)((selectedImage).c_str()));
		HWND button = FindWindowEx(hwnd, NULL, L"Button", NULL);
		SendMessage(hwnd, WM_COMMAND, 1, (LPARAM)button);
	}
	return true;
}