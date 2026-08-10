// dllmain.cpp : 定义 DLL 应用程序的入口点。
#include "pch.h"
#include "dllmain.h"
//#include "screenscale.cpp"
#include "inicpp.hpp"
#include<iostream>
#include <set>

using namespace inicpp;

BOOL APIENTRY DllMain(HMODULE hModule,
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

int getScreenW()
{
	int screenW = ::GetSystemMetrics(SM_CXSCREEN);
	return screenW;

}
bool gethdc()
{
	HWND hwd = ::GetDesktopWindow();
	HDC hdc = ::GetDC(hwd);
	if (!hdc) {
		return false;

	}
	::ReleaseDC(hwd, hdc); // 必须释放 DC
	return true;

}
int getWidth()
{
	HWND hwd = GetDesktopWindow();

	HDC hdc = GetDC(hwd);
	int width = ::GetDeviceCaps(hdc, DESKTOPHORZRES);
	return width;

}

static int CaptureAnImage(HWND hWnd, const float& scale, const wchar_t* name = L"")
{
	HDC hdcScreen;
	HDC hdcWindow;
	HDC hdcMemDC = NULL;
	HBITMAP hbmScreen = NULL;
	BITMAP bmpScreen;
	DWORD dwBytesWritten = 0;
	DWORD dwSizeofDIB = 0;
	HANDLE hFile = NULL;
	char* lpbitmap = NULL;
	HANDLE hDIB = NULL;
	DWORD dwBmpSize = 0;

	// Retrieve the handle to a display device context for the client 
	// area of the window. 
	hdcScreen = GetDC(NULL);
	hdcWindow = GetDC(hWnd);

	// Create a compatible DC, which is used in a BitBlt from the window DC.
	hdcMemDC = CreateCompatibleDC(hdcWindow);

	if (!hdcMemDC)
	{
		MessageBox(hWnd, L"CreateCompatibleDC has failed", L"Failed", MB_OK);
		goto done;
	}

	// Get the client area for size calculation.
	RECT rcClient;
	GetClientRect(hWnd, &rcClient);

	// This is the best stretch mode.
	SetStretchBltMode(hdcWindow, HALFTONE);

	// The source DC is the entire screen, and the destination DC is the current window (HWND).
	if (!StretchBlt(hdcWindow,
		0, 0,
		rcClient.right, rcClient.bottom,
		hdcScreen,
		0, 0,
		GetSystemMetrics(SM_CXSCREEN),
		GetSystemMetrics(SM_CYSCREEN),
		SRCCOPY))
	{
		MessageBox(hWnd, L"StretchBlt has failed", L"Failed", MB_OK);
		goto done;
	}
	//Screen Scale


	rcClient.bottom *= scale;
	rcClient.top *= scale;
	rcClient.left *= scale;
	rcClient.right *= scale;

	// Create a compatible bitmap from the Window DC.
	hbmScreen = CreateCompatibleBitmap(hdcWindow, rcClient.right - rcClient.left, rcClient.bottom - rcClient.top);

	if (!hbmScreen)
	{
		MessageBox(hWnd, L"CreateCompatibleBitmap Failed", L"Failed", MB_OK);
		goto done;
	}

	// Select the compatible bitmap into the compatible memory DC.
	SelectObject(hdcMemDC, hbmScreen);

	// Bit block transfer into our compatible memory DC.
	if (!BitBlt(hdcMemDC,
		0, 0,
		rcClient.right - rcClient.left, rcClient.bottom - rcClient.top,
		hdcWindow,
		0, 0,
		SRCCOPY))
	{
		MessageBox(hWnd, L"BitBlt has failed", L"Failed", MB_OK);
		goto done;
	}

	// Get the BITMAP from the HBITMAP.
	GetObject(hbmScreen, sizeof(BITMAP), &bmpScreen);

	BITMAPFILEHEADER   bmfHeader;
	BITMAPINFOHEADER   bi;

	bi.biSize = sizeof(BITMAPINFOHEADER);
	bi.biWidth = bmpScreen.bmWidth;
	bi.biHeight = bmpScreen.bmHeight;
	bi.biPlanes = 1;
	bi.biBitCount = 32;
	bi.biCompression = BI_RGB;
	bi.biSizeImage = 0;
	bi.biXPelsPerMeter = 0;
	bi.biYPelsPerMeter = 0;
	bi.biClrUsed = 0;
	bi.biClrImportant = 0;

	dwBmpSize = ((bmpScreen.bmWidth * bi.biBitCount + 31) / 32) * 4 * bmpScreen.bmHeight;

	// Starting with 32-bit Windows, GlobalAlloc and LocalAlloc are implemented as wrapper functions that 
	// call HeapAlloc using a handle to the process's default heap. Therefore, GlobalAlloc and LocalAlloc 
	// have greater overhead than HeapAlloc.
	hDIB = GlobalAlloc(GHND, dwBmpSize);
	lpbitmap = (char*)GlobalLock(hDIB);

	// Gets the "bits" from the bitmap, and copies them into a buffer 
	// that's pointed to by lpbitmap.
	GetDIBits(hdcWindow, hbmScreen, 0,
		(UINT)bmpScreen.bmHeight,
		lpbitmap,
		(BITMAPINFO*)&bi, DIB_RGB_COLORS);

	// A file is created, this is where we will save the screen capture.
	hFile = CreateFile(name,
		GENERIC_WRITE,
		0,
		NULL,
		CREATE_ALWAYS,
		FILE_ATTRIBUTE_NORMAL, NULL);

	// Add the size of the headers to the size of the bitmap to get the total file size.
	dwSizeofDIB = dwBmpSize + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

	// Offset to where the actual bitmap bits start.
	bmfHeader.bfOffBits = (DWORD)sizeof(BITMAPFILEHEADER) + (DWORD)sizeof(BITMAPINFOHEADER);

	// Size of the file.
	bmfHeader.bfSize = dwSizeofDIB;

	// bfType must always be BM for Bitmaps.
	bmfHeader.bfType = 0x4D42; // BM.

	WriteFile(hFile, (LPSTR)&bmfHeader, sizeof(BITMAPFILEHEADER), &dwBytesWritten, NULL);
	WriteFile(hFile, (LPSTR)&bi, sizeof(BITMAPINFOHEADER), &dwBytesWritten, NULL);
	WriteFile(hFile, (LPSTR)lpbitmap, dwBmpSize, &dwBytesWritten, NULL);

	// Unlock and Free the DIB from the heap.
	GlobalUnlock(hDIB);
	GlobalFree(hDIB);

	// Close the handle for the file that was created.
	CloseHandle(hFile);

	// Clean up.
done:
	DeleteObject(hbmScreen);
	DeleteObject(hdcMemDC);
	ReleaseDC(NULL, hdcScreen);
	ReleaseDC(hWnd, hdcWindow);

	return 0;
}
static bool fileExists(const wchar_t* path)
{
	DWORD attributes = GetFileAttributes(path);
	return (attributes != INVALID_FILE_ATTRIBUTES && !(attributes & FILE_ATTRIBUTE_DIRECTORY));
}
extern "C" __declspec(dllexport)
int fullScreenshot()
{
	float scale = 1.0f;
	if (gethdc())
	{
		scale = float(getWidth()) / getScreenW();
	}
	//CaptureAnImage(GetDesktopWindow(), scale, L"screenshot.bmp");
	screenshot(0, 0, getWidth(), getScreenW());
	if (not fileExists(L"screenshot.png"))
	{
		return 1;
	}
	return 0;
}
std::optional<unsigned char*> cropImage(
	const unsigned char* src_data,
	int src_w, int src_h, int channels,
	int crop_x, int crop_y, int crop_w, int crop_h)
{
	// 1. 边界检查与修正
	if (crop_x < 0) crop_x = 0;
	if (crop_y < 0) crop_y = 0;

	// 如果起点就在图片外，直接失败
	if (crop_x >= src_w || crop_y >= src_h) {
		return std::nullopt; 
	}

	// 修正裁剪尺寸以防止越界
	if (crop_x + crop_w > src_w) crop_w = src_w - crop_x;
	if (crop_y + crop_h > src_h) crop_h = src_h - crop_y;

	if (crop_w <= 0 || crop_h <= 0) {
		return std::nullopt;
	}

	// 2. 分配内存 (调用者负责 delete[])
	// 注意：使用 new[] 而不是 new，因为我们要分配数组
	unsigned char* destData = new(std::nothrow) unsigned char[crop_w * crop_h * channels];
	if (!destData) {
		return std::nullopt; // 内存分配失败
	}

	const int src_row_stride = src_w * channels;
	const int dst_row_stride = crop_w * channels;
	const int copy_bytes = dst_row_stride;

	// 3. 逐行拷贝
	for (int y = 0; y < crop_h; ++y) {
		const unsigned char* src_row_ptr = src_data + ((crop_y + y) * src_row_stride) + (crop_x * channels);
		unsigned char* dst_row_ptr = destData + (y * dst_row_stride);
		std::memcpy(dst_row_ptr, src_row_ptr, copy_bytes);
	}

	return destData;
}

extern "C" __declspec(dllexport)
int screenshot(int left, int top, int width, int height)
{
	// 1. 计算缩放比例
	float scale = 1.0f;
	if (gethdc()) {
		// 防止除以零
		int screenW = getScreenW();
		if (screenW > 0) {
			scale = static_cast<float>(getWidth()) / screenW;
		}
	}

	const wchar_t* temp_file = L"captureqwsx.bmp";
	const char* out_file = "screenshot.png";

	// 2. 截图
	CaptureAnImage(GetDesktopWindow(), scale, temp_file);

	if (!fileExists(temp_file)) {
		return 1; // 截图失败
	}

	// 3. 加载图片
	int img_w, img_h, channels;
	unsigned char* image = stbi_load("captureqwsx.bmp", &img_w, &img_h, &channels, 0);

	if (!image) {
		return 2; // 加载图片失败
	}

	// 4. 执行裁剪
	// 传入正确的原图尺寸 (img_w, img_h) 和 用户想要的裁剪参数 (left, top, width, height)
	auto cropped_opt = cropImage(image, img_w, img_h, channels, left, top, width, height);

	// 释放源图片内存 (stb_image 分配的必须用 stbi_image_free)
	stbi_image_free(image);
	bool success=DeleteFileW(temp_file);
	if (!success)
	{
		std::cout<<"失败" << GetLastError() << std::endl;;
	}

	if (!cropped_opt.has_value()) {
		// 裁剪失败 (可能是区域越界)
		return 3;
	}

	unsigned char* cropped_ptr = cropped_opt.value();

	int final_w = width;
	int final_h = height;

	// 简单的边界钳制逻辑复现，确保写入尺寸正确
	if (left < 0) left = 0;
	if (top < 0) top = 0;
	if (left + final_w > img_w) final_w = img_w - left;
	if (top + final_h > img_h) final_h = img_h - top;

	if (final_w <= 0 || final_h <= 0) {
		delete[] cropped_ptr; // 清理内存
		return 3;
	}

	bool write_success = stbi_write_png(out_file, final_w, final_h, channels, cropped_ptr,0);

	// 6. 清理内存 (对应 cropImage 中的 new[])
	// 无论保存是否成功，都必须删除，防止内存泄漏
	delete[] cropped_ptr;

	if (!write_success) {
		return 4; // 保存失败
	}

	return 0; // 成功
}
