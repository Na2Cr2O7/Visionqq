
// MFCUpdateDlg.cpp: 实现文件
//

#include "pch.h"
#include "framework.h"
#include "MFCUpdate.h"
#include "MFCUpdateDlg.h"
#include "afxdialogex.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif


#include <generator>       //C++23
#include <filesystem>
#include <ranges>
#include <cctype>
std::generator<std::filesystem::path> recursiveFiles(std::filesystem::path path)
{
	try
	{
		for (auto& p : std::filesystem::recursive_directory_iterator(path))
		{
			co_yield p.path();

			//if (p.is_regular_file())
			//{
			//	co_yield p.path();
			//}
		}

	}
	catch (std::filesystem::filesystem_error& e)
	{

	}

}
#include <filesystem>
#include <generator>
#include <utility>
static std::generator< std::pair<std::filesystem::path, bool> > recursiveSubdirectoriesFilesX(std::filesystem::path path)
{
	try
	{
		for (auto& p : std::filesystem::recursive_directory_iterator(path))
		{
			std::error_code ec;
			
			co_yield std::make_pair(std::filesystem::relative(path,p), p.is_regular_file(ec));
		}

	}
	catch (std::filesystem::filesystem_error& e)
	{

	}
}
std::generator<std::pair<std::filesystem::path, bool>>
recursiveSubdirectoriesFiles(std::filesystem::path path)
{
	std::error_code ec;
	auto canonical_path = std::filesystem::canonical(path, ec);
	if (ec) {
		// 如果 canonical 失败（比如路径不存在），回退到 absolute 或直接使用原 path
		canonical_path = std::filesystem::absolute(path, ec);
		if (ec) {
			// 无法解析路径，可能直接返回空
			co_return;
		}
	}

	try {
		for (const auto& p : std::filesystem::recursive_directory_iterator(canonical_path, ec)) {
			if (ec) {
				// 忽略单个条目的错误（如权限不足）
				continue;
			}

			// 计算相对于原始 path 的相对路径
			auto rel = std::filesystem::relative(p.path(), canonical_path, ec);
			if (ec) {
				// 如果无法计算相对路径，跳过
				continue;
			}

			// 安全地检查是否为普通文件
			bool is_file = p.is_regular_file(ec);
			if (ec) {
				// 如果无法确定类型，视为非文件（或根据需求处理）
				is_file = false;
			}

			co_yield std::make_pair(rel, is_file);
		}
	}
	catch (const std::filesystem::filesystem_error&) {
		// 忽略顶层迭代异常（通常不会触发，因为用了 error_code）
	}
}

// CMFCUpdateDlg 对话框



CMFCUpdateDlg::CMFCUpdateDlg(CWnd* pParent /*=nullptr*/)
	: CDialogEx(IDD_MFCUPDATE_DIALOG, pParent)
{
	m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
}

void CMFCUpdateDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
	DDX_Control(pDX, IDC_BUTTON1, Sel);
	DDX_Control(pDX, IDC_EDIT1, PathEdit);
	DDX_Control(pDX, IDC_EDIT2, VersionText);
}

BEGIN_MESSAGE_MAP(CMFCUpdateDlg, CDialogEx)
	ON_WM_PAINT()
	ON_WM_QUERYDRAGICON()
	ON_BN_CLICKED(IDOK, &CMFCUpdateDlg::OnBnClickedOk)
	ON_BN_CLICKED(IDC_BUTTON1, &CMFCUpdateDlg::OnBnClickedButton1)
	ON_EN_CHANGE(IDC_EDIT1, &CMFCUpdateDlg::OnEnChangeEdit1)
	ON_BN_CLICKED(IDC_BUTTON2, &CMFCUpdateDlg::OnBnClickedButton2)
END_MESSAGE_MAP()


// CMFCUpdateDlg 消息处理程序

BOOL CMFCUpdateDlg::OnInitDialog()
{
	CDialogEx::OnInitDialog();

	// 设置此对话框的图标。  当应用程序主窗口不是对话框时，框架将自动
	//  执行此操作
	SetIcon(m_hIcon, TRUE);			// 设置大图标
	SetIcon(m_hIcon, FALSE);		// 设置小图标

	// TODO: 在此添加额外的初始化代码
	using namespace inicpp;

	auto newIni = std::make_unique<IniManager>("config.ini");
	std::string version2 = (*newIni)["general"]["version"];
	newIni.release();
	int bufferSize = MultiByteToWideChar(CP_UTF8, 0, version2.c_str(), -1, NULL, 0);
	std::unique_ptr<wchar_t> wVersion=std::make_unique<wchar_t>(bufferSize);
	MultiByteToWideChar(CP_UTF8, 0, version2.c_str(), -1, wVersion.get(),bufferSize);

	/*CString version = reinterpret_cast<const wchar_t*>((static_cast<std::string>((*newIni)["general"]["version"])).c_str());*/
	VersionText.SetWindowTextW(wVersion.get());
	wVersion.release();

	return TRUE;  // 除非将焦点设置到控件，否则返回 TRUE
}

// 如果向对话框添加最小化按钮，则需要下面的代码
//  来绘制该图标。  对于使用文档/视图模型的 MFC 应用程序，
//  这将由框架自动完成。

void CMFCUpdateDlg::OnPaint()
{
	if (IsIconic())
	{
		CPaintDC dc(this); // 用于绘制的设备上下文

		SendMessage(WM_ICONERASEBKGND, reinterpret_cast<WPARAM>(dc.GetSafeHdc()), 0);

		// 使图标在工作区矩形中居中
		int cxIcon = GetSystemMetrics(SM_CXICON);
		int cyIcon = GetSystemMetrics(SM_CYICON);
		CRect rect;
		GetClientRect(&rect);
		int x = (rect.Width() - cxIcon + 1) / 2;
		int y = (rect.Height() - cyIcon + 1) / 2;

		// 绘制图标
		dc.DrawIcon(x, y, m_hIcon);
	}
	else
	{
		CDialogEx::OnPaint();
	}
}

//当用户拖动最小化窗口时系统调用此函数取得光标
//显示。
HCURSOR CMFCUpdateDlg::OnQueryDragIcon()
{
	return static_cast<HCURSOR>(m_hIcon);
}


void CMFCUpdateDlg::OnBnClickedOk()
{
	// TODO: 在此添加控件通知处理程序代码
	CDialogEx::OnOK();
}

using namespace inicpp;
void CMFCUpdateDlg::OnBnClickedButton1()
{
	setlocale(LC_ALL, "zh_CN.UTF-8");
	const char* general = "general";

	CFolderPickerDialog folderDlg;
	if (folderDlg.DoModal() == IDOK)
	{
		CString strFolderPath = folderDlg.GetFolderPath();
		// 显示或使用路径

		(this->PathEdit).SetWindowTextW(strFolderPath);
		CString destPath;
		(this->PathEdit).GetWindowTextW(destPath);
	}


}

void CMFCUpdateDlg::OnEnChangeEdit1()
{
	// TODO:  如果该控件是 RICHEDIT 控件，它将不
	// 发送此通知，除非重写 CDialogEx::OnInitDialog()
	// 函数并调用 CRichEditCtrl().SetEventMask()，
	// 同时将 ENM_CHANGE 标志“或”运算到掩码中。

	// TODO:  在此添加控件通知处理程序代码
}
constexpr auto CONFIG_FILE = "config.ini";
//constexpr auto LCONFIG_FILE = L"config.ini";
void CMFCUpdateDlg::OnBnClickedButton2()
{
	setlocale(LC_ALL, "zh_CN.UTF-8");
	const char* general = "general";

	CString destPath;
	(this->PathEdit).GetWindowTextW(destPath);
	std::wstring oldIniPath = destPath.GetBuffer();
	//std::wstring_view oldPath(oldIniPath);
	oldIniPath += L"\\config.ini";
	auto newIni = std::make_unique<IniManager>(CONFIG_FILE);
	//IniManager* newIni = new IniManager("config.ini");



	int bufferSize = WideCharToMultiByte(CP_UTF8, 0, oldIniPath.c_str(), -1, NULL, 0, NULL, NULL);
	std::unique_ptr<char> path2 = std::make_unique<char>(bufferSize);		

	//char* path2 = new char[bufferSize];

	WideCharToMultiByte(CP_UTF8, 0, oldIniPath.c_str(), -1, path2.get(), bufferSize, NULL, NULL);
	std::string_view oldPath(path2.get(), path2.get() + bufferSize - (std::strlen(CONFIG_FILE)+1));

	//IniManager* oldIni = new IniManager(path2.get());
	auto oldIni = std::make_unique<IniManager>(path2.get());

	std::string version = (*newIni)[general]["version"];
	for (auto& kv : oldIni->sectionMap(general))
	{
		newIni->set(general, kv.first, kv.second);
	}
	newIni->set(general, "version", version);
	/*oldIni.reset();*/
	//newIni.reset();
	//delete oldIni;
	//delete newIni;
	oldIni.release();
	newIni.release();

	//读取system.txt(1.5.11+)
	try
	{
		std::ifstream src(std::string(oldPath)+"system.txt", std::ios::binary);
		std::ofstream dst("system.txt", std::ios::binary);
		dst << src.rdbuf();
	}
	catch(std::exception e)
	{

	}


	auto files2 = recursiveFiles(std::filesystem::current_path());
	std::vector< std::filesystem::path> E;
	for (auto file : files2)
	{
		E.push_back(file);

	}

	for (auto file : E )
	{
		std::filesystem::path dest(oldPath);

		try
		{	
			dest /= std::filesystem::relative(file, std::filesystem::current_path());
			if (std::filesystem::is_directory(file))
			{
				
					try {

						std::filesystem::create_directories(dest);
					}
					catch (std::exception e)
					{
						//MessageBoxA(NULL, e.what(), "提示", MB_OK);
					}
	
			}

			//auto r = file;
			//std::filesystem::copy_file(file,dest);
			//char* fileC=;
			bool success=CopyFileA(file.string().c_str(), dest.string().c_str(), false);
			//int bufferSize = MultiByteToWideChar(CP_UTF8, 0, file.string().c_str(), -1, NULL, 0);
			//std::unique_ptr<wchar_t> wInfo = std::make_unique<wchar_t>(bufferSize);
			//MultiByteToWideChar(CP_UTF8, 0, file.string().c_str(), -1, wInfo.get(), bufferSize);
			//this->VersionText.SetWindowTextW(wInfo.get());
			//wInfo.release();


			if (!success)
			{
				auto t=std::to_string(GetLastError());
				throw std::exception();
			}

		}
		catch (std::exception e)
		{
			//MessageBoxA(NULL, e.what(), "错误", MB_OK | MB_ICONERROR);

		  }


	}
	path2.release();
	MessageBox(L"", L"升级成功", MB_OK | MB_ICONASTERISK);
}
