#pragma once
#include <Windows.h>
#include <iostream>
#include "Point.hpp"

namespace positions
{


	// 默认尺寸
	constexpr  static int DEFAULT_WIDTH = 2240;
	constexpr static int DEFAULT_HEIGHT = 1260;
	constexpr static  double SCALE = 10000.0;


	// 绝对坐标尺寸
	RECT chatListBBoxAbsoluteSize = { 105, 154, 105 + 305, 154 + 1055 };
	RECT conversationBBoxAbsoluteSize = { 421, 163, 421 + 1796, 163 + 734 };
	RECT sendButtonBBoxAbsoluteSize = { 2023, 1167, 2023 + 182, 1167 + 79 };
	RECT commentSectionBBoxAbsoluteSize = { 563, 963, 563 + 1455, 963 + 271 };
	RECT exitConversationBBoxAbsoluteSize = { 367, 228, 367 + 31, 228 + 33 };
	RECT sendImageBBoxAbsoluteSize = { 663, 917, 663 + 44, 917 + 44 };
	RECT copyButtonBBoxAbsoluteSize = { 1698, 1028, 1698 + 52, 1028 + 45 };

	Point startDraggingAbsolutePosition = { 2151, 852 };
	Point endDraggingAbsolutePosition = { 435, 0 };

	// 相对坐标尺寸计算
	RECT CHAT_LIST_BBOX_RELATIVE_SIZE = {
		(long)(chatListBBoxAbsoluteSize.left * SCALE / DEFAULT_WIDTH) / SCALE,
		(long)(chatListBBoxAbsoluteSize.top * SCALE / DEFAULT_HEIGHT) / SCALE,
		(long)(chatListBBoxAbsoluteSize.right * SCALE / DEFAULT_WIDTH) / SCALE,
		(long)(chatListBBoxAbsoluteSize.bottom * SCALE / DEFAULT_HEIGHT) / SCALE
	};

	RECT CONVERSATION_BBOX_RELATIVE_SIZE = {
		(long)(conversationBBoxAbsoluteSize.left * SCALE / DEFAULT_WIDTH) / SCALE,
		(long)(conversationBBoxAbsoluteSize.top * SCALE / DEFAULT_HEIGHT) / SCALE,
		(long)(conversationBBoxAbsoluteSize.right * SCALE / DEFAULT_WIDTH) / SCALE,
		(long)(conversationBBoxAbsoluteSize.bottom * SCALE / DEFAULT_HEIGHT) / SCALE
	};

	RECT SEND_BUTTON_BBOX_RELATIVE_SIZE = {
		(long)(sendButtonBBoxAbsoluteSize.left * SCALE / DEFAULT_WIDTH) / SCALE,
		(long)(sendButtonBBoxAbsoluteSize.top * SCALE / DEFAULT_HEIGHT) / SCALE,
		(long)(sendButtonBBoxAbsoluteSize.right * SCALE / DEFAULT_WIDTH) / SCALE,
		(long)(sendButtonBBoxAbsoluteSize.bottom * SCALE / DEFAULT_HEIGHT) / SCALE
	};

	RECT COMMENT_SECTION_BBOX_RELATIVE_SIZE = {
		(long)(commentSectionBBoxAbsoluteSize.left * SCALE / DEFAULT_WIDTH) / SCALE,
		(long)(commentSectionBBoxAbsoluteSize.top * SCALE / DEFAULT_HEIGHT) / SCALE,
		(long)(commentSectionBBoxAbsoluteSize.right * SCALE / DEFAULT_WIDTH) / SCALE,
		(long)(commentSectionBBoxAbsoluteSize.bottom * SCALE / DEFAULT_HEIGHT) / SCALE
	};

	RECT EXIT_CONVERSATION_BBOX_RELATIVE_SIZE = {
		(long)(exitConversationBBoxAbsoluteSize.left * SCALE / DEFAULT_WIDTH) / SCALE,
		(long)(exitConversationBBoxAbsoluteSize.top * SCALE / DEFAULT_HEIGHT) / SCALE,
		(long)(exitConversationBBoxAbsoluteSize.right * SCALE / DEFAULT_WIDTH) / SCALE,
		(long)(exitConversationBBoxAbsoluteSize.bottom * SCALE / DEFAULT_HEIGHT) / SCALE
	};

	RECT SEND_IMAGE_BBOX_RELATIVE_SIZE = {
		(long)(sendImageBBoxAbsoluteSize.left * SCALE / DEFAULT_WIDTH) / SCALE,
		(long)(sendImageBBoxAbsoluteSize.top * SCALE / DEFAULT_HEIGHT) / SCALE,
		(long)(sendImageBBoxAbsoluteSize.right * SCALE / DEFAULT_WIDTH) / SCALE,
		(long)(sendImageBBoxAbsoluteSize.bottom * SCALE / DEFAULT_HEIGHT) / SCALE
	};

	RECT COPY_BUTTON_BBOX_RELATIVE_SIZE = {
		(long)(copyButtonBBoxAbsoluteSize.left * SCALE / DEFAULT_WIDTH) / SCALE,
		(long)(copyButtonBBoxAbsoluteSize.top * SCALE / DEFAULT_HEIGHT) / SCALE,
		(long)(copyButtonBBoxAbsoluteSize.right * SCALE / DEFAULT_WIDTH) / SCALE,
		(long)(copyButtonBBoxAbsoluteSize.bottom * SCALE / DEFAULT_HEIGHT) / SCALE
	};

	// 转换为实际尺寸的函数
	RECT toActualSize(const RECT& relativeSize,const int width,const int height) {
		RECT actualSize;
		actualSize.left = (long)(relativeSize.left * width);
		actualSize.top = (long)(relativeSize.top * height);
		actualSize.right = (long)(relativeSize.right * width);
		actualSize.bottom = (long)(relativeSize.bottom * height);
		return actualSize;
	}

	Point toActualPoint(const Point& relativePoint,const int width,const int height) {
		Point actualPoint;
		actualPoint.x = (short)(relativePoint.x * width / SCALE);
		actualPoint.y = (short)(relativePoint.y * height / SCALE);
		return actualPoint;
	}

	// 输出调试信息的函数
	void printDebugInfo() {
		std::cout << "chatListBBoxRelativeSize: ("
			<< CHAT_LIST_BBOX_RELATIVE_SIZE.left << ", "
			<< CHAT_LIST_BBOX_RELATIVE_SIZE.top << ", "
			<< CHAT_LIST_BBOX_RELATIVE_SIZE.right << ", "
			<< CHAT_LIST_BBOX_RELATIVE_SIZE.bottom << ")" << std::endl;

		std::cout << "conversationBBoxRelativeSize: ("
			<< CONVERSATION_BBOX_RELATIVE_SIZE.left << ", "
			<< CONVERSATION_BBOX_RELATIVE_SIZE.top << ", "
			<< CONVERSATION_BBOX_RELATIVE_SIZE.right << ", "
			<< CONVERSATION_BBOX_RELATIVE_SIZE.bottom << ")" << std::endl;

		std::cout << "sendButtonBBoxRelativeSize: ("
			<< SEND_BUTTON_BBOX_RELATIVE_SIZE.left << ", "
			<< SEND_BUTTON_BBOX_RELATIVE_SIZE.top << ", "
			<< SEND_BUTTON_BBOX_RELATIVE_SIZE.right << ", "
			<< SEND_BUTTON_BBOX_RELATIVE_SIZE.bottom << ")" << std::endl;

		std::cout << "commentSectionBBoxRelativeSize: ("
			<< COMMENT_SECTION_BBOX_RELATIVE_SIZE.left << ", "
			<< COMMENT_SECTION_BBOX_RELATIVE_SIZE.top << ", "
			<< COMMENT_SECTION_BBOX_RELATIVE_SIZE.right << ", "
			<< COMMENT_SECTION_BBOX_RELATIVE_SIZE.bottom << ")" << std::endl;

		std::cout << "exitConversationBBoxRelativeSize: ("
			<< EXIT_CONVERSATION_BBOX_RELATIVE_SIZE.left << ", "
			<< EXIT_CONVERSATION_BBOX_RELATIVE_SIZE.top << ", "
			<< EXIT_CONVERSATION_BBOX_RELATIVE_SIZE.right << ", "
			<< EXIT_CONVERSATION_BBOX_RELATIVE_SIZE.bottom << ")" << std::endl;

		std::cout << "sendImageBBoxRelativeSize: ("
			<< SEND_IMAGE_BBOX_RELATIVE_SIZE.left << ", "
			<< SEND_IMAGE_BBOX_RELATIVE_SIZE.top << ", "
			<< SEND_IMAGE_BBOX_RELATIVE_SIZE.right << ", "
			<< SEND_IMAGE_BBOX_RELATIVE_SIZE.bottom << ")" << std::endl;

		std::cout << "copyButtonBBoxRelativeSize: ("
			<< COPY_BUTTON_BBOX_RELATIVE_SIZE.left << ", "
			<< COPY_BUTTON_BBOX_RELATIVE_SIZE.top << ", "
			<< COPY_BUTTON_BBOX_RELATIVE_SIZE.right << ", "
			<< COPY_BUTTON_BBOX_RELATIVE_SIZE.bottom << ")" << std::endl;
	}
}