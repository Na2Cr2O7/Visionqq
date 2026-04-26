var imageDir = Path.Combine(System.AppDomain.CurrentDomain.BaseDirectory, "Images");
Console.WriteLine(imageDir);

List<string> dirs = [.. Directory.EnumerateFiles(imageDir)];
bool containsImage = false;


// 定义支持的图像扩展名（可根据需要调整）
var imageExtensions = new HashSet<string>(StringComparer.OrdinalIgnoreCase)
                        {
                            ".jpg", ".jpeg", ".png", ".gif"
                        };

foreach (string dir in dirs)
{
    Console.WriteLine(dir);

        if (imageExtensions.Contains(Path.GetExtension(dir)))
        {
            containsImage = true;
            Console.WriteLine("Image:", dir);
            break;
        }

}
Console.WriteLine(containsImage);