using System;
using System.Diagnostics;
namespace QQPilot4
{
public static class QQChatUIConstants
{
    // 默认分辨率
    public static readonly (int Width, int Height) DEFAULT_SIZE = (2240, 1260);
    public static readonly (int Width, int Height) DEFAULT_SIZE2 = (1280, 720);

    // 绝对坐标定义（x1, y1, x2, y2）
    public static readonly (int, int, int, int) chatListBBoxAbsoluteSize = (105, 154, 105 + 305, 154 + 1055);
    public static readonly (int, int, int, int) conversationBBoxAbsoluteSize = (421, 163, 421 + 1796, 163 + 734);
    public static readonly (int, int, int, int) sendButtonBBoxAbsoluteSize = (2023, 1167, 2023 + 182, 1167 + 79);
    public static readonly (int, int, int, int) commentSectionBBoxAbsoluteSize = (563, 963, 563 + 1455, 963 + 271);
    public static readonly (int, int, int, int) exitConversationBBoxAbsoluteSize = (367, 228, 367 + 31, 228 + 33);
    public static readonly (int, int, int, int) sendImageBBoxAbsoluteSize = (663, 917, 663 + 44, 917 + 44);
    public static readonly (int, int, int, int) copyButtonBBoxAbsoluteSize = (1698, 1028, 1698 + 52, 1028 + 45);
    public static readonly (int, int, int, int) atPlaceBBoxAbsoluteSize = (108, 160, 108 + 165, 180 + 1099);
    public static readonly (int, int, int, int) uploadImagePossibleBBoxAbsoluteSize = (546, 885, 546 + 784, 885 + 188);
    public static readonly (int, int, int, int) copyButtonPossibleBBoxAbsoluteSize = (525, 912, 525 + 1121, 912 + 283);

    // 拖拽与取消按钮位置
    public static readonly (int, int) startDraggingAbsolutePosition = (1898, 882);
    public static readonly (int, int) endDraggingAbsolutePosition = (435, 0);
    public static readonly (int, int) cancelButtonAbsolutePosition = (1325, 697);

    // DEFAULT_SIZE2 下的按钮位置
    public static readonly (int, int) contactButtonAbsolutePosition = (28, 104);
    public static readonly (int, int) chatButtonAbsolutePosition = (27, 63);

    // 相对坐标计算（基于 DEFAULT_SIZE）
    public static readonly (double, double, double, double) CHAT_LIST_BBOX_RELATIVE_SIZE =
        ToRelativeRect(chatListBBoxAbsoluteSize, DEFAULT_SIZE);

    public static readonly (double, double, double, double) CONVERSATION_BBOX_RELATIVE_SIZE =
        ToRelativeRect(conversationBBoxAbsoluteSize, DEFAULT_SIZE);

    public static readonly (double, double, double, double) SEND_BUTTON_BBOX_RELATIVE_SIZE =
        ToRelativeRect(sendButtonBBoxAbsoluteSize, DEFAULT_SIZE);

    public static readonly (double, double, double, double) COMMENT_SECTION_BBOX_RELATIVE_SIZE =
        ToRelativeRect(commentSectionBBoxAbsoluteSize, DEFAULT_SIZE);

    public static readonly (double, double, double, double) EXIT_CONVERSATION_BBOX_RELATIVE_SIZE =
        ToRelativeRect(exitConversationBBoxAbsoluteSize, DEFAULT_SIZE);

    public static readonly (double, double, double, double) SEND_IMAGE_BBOX_RELATIVE_SIZE =
        ToRelativeRect(sendImageBBoxAbsoluteSize, DEFAULT_SIZE);

    public static readonly (double, double, double, double) COPY_BUTTON_BBOX_RELATIVE_SIZE =
        ToRelativeRect(copyButtonBBoxAbsoluteSize, DEFAULT_SIZE);

    public static readonly (double, double, double, double) AT_PLACE_BBOX_RELATIVE_SIZE =
        ToRelativeRect(atPlaceBBoxAbsoluteSize, DEFAULT_SIZE);

    public static readonly (double, double, double, double) UPLOAD_IMAGE_POSSIBLE_BBOX_RELATIVE_SIZE =
        ToRelativeRect(uploadImagePossibleBBoxAbsoluteSize, DEFAULT_SIZE);

    public static readonly (double, double, double, double) COPY_BUTTON_POSSIBLE_BBOX_RELATIVE_SIZE =
        ToRelativeRect(copyButtonPossibleBBoxAbsoluteSize, DEFAULT_SIZE);

    // 相对点位置
    public static readonly (double, double) START_DRAGGING_RELATIVE_POSITION =
        ToRelativePoint(startDraggingAbsolutePosition, DEFAULT_SIZE);

    public static readonly (double, double) END_DRAGGING_RELATIVE_POSITION =
        ToRelativePoint(endDraggingAbsolutePosition, DEFAULT_SIZE);

    public static readonly (double, double) CANCEL_BUTTON_RELATIVE_POSITION =
        ToRelativePoint(cancelButtonAbsolutePosition, DEFAULT_SIZE);

    public static readonly (double, double) CONTACT_BUTTON_RELATIVE_POSITION =
        ToRelativePoint(contactButtonAbsolutePosition, DEFAULT_SIZE2);

    public static readonly (double, double) CHAT_BUTTON_RELATIVE_POSITION =
        ToRelativePoint(chatButtonAbsolutePosition, DEFAULT_SIZE2);

    // 辅助方法：将绝对矩形转为相对矩形 (x1, y1, x2, y2)
    private static (double, double, double, double) ToRelativeRect((int x1, int y1, int x2, int y2) rect, (int Width, int Height) size)
    {
        return (
            rect.x1 / (double)size.Width,
            rect.y1 / (double)size.Height,
            rect.x2 / (double)size.Width,
            rect.y2 / (double)size.Height
        );
    }

    // 辅助方法：将绝对点转为相对点
    private static (double, double) ToRelativePoint((int x, int y) point, (int Width, int Height) size)
    {
        return (
            point.x / (double)size.Width,
            point.y / (double)size.Height
        );
    }

    // 转换回实际尺寸：从相对矩形到绝对矩形
    public static (int, int, int, int) ToActualSize((double x1, double y1, double x2, double y2) relativeRect, (int Width, int Height) size)
    {
        return (
            (int)Math.Round(relativeRect.x1 * size.Width),
            (int)Math.Round(relativeRect.y1 * size.Height),
            (int)Math.Round(relativeRect.x2 * size.Width),
            (int)Math.Round(relativeRect.y2 * size.Height)
        );
    }

    // 转换回实际点：从相对点到绝对点
    public static (int, int) ToActualPoint((double x, double y) relativePoint, (int Width, int Height) size)
    {
        return (
            (int)Math.Round(relativePoint.x * size.Width),
            (int)Math.Round(relativePoint.y * size.Height)
        );
    }

    // 初始化时输出调试日志（模拟 logging.debug）
    static QQChatUIConstants()
    {
        Debug.WriteLine($"chatListBBoxRelativeSize: {CHAT_LIST_BBOX_RELATIVE_SIZE}");
        Debug.WriteLine($"conversationBBoxRelativeSize: {CONVERSATION_BBOX_RELATIVE_SIZE}");
        Debug.WriteLine($"sendButtonBBoxRelativeSize: {SEND_BUTTON_BBOX_RELATIVE_SIZE}");
        Debug.WriteLine($"commentSectionBBoxRelativeSize: {COMMENT_SECTION_BBOX_RELATIVE_SIZE}");
        Debug.WriteLine($"exitConversationBBoxRelativeSize: {EXIT_CONVERSATION_BBOX_RELATIVE_SIZE}");
        Debug.WriteLine($"sendImageBBoxRelativeSize: {SEND_IMAGE_BBOX_RELATIVE_SIZE}");
        Debug.WriteLine($"copyButtonBBoxRelativeSize: {COPY_BUTTON_BBOX_RELATIVE_SIZE}");
    }
}

}
