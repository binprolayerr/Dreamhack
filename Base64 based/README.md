https://dreamhack.io/wargame/challenges/1785

Bài này ta được cho đoạn mã sau:
```php
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Loader</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            max-width: 600px;
            width: 100%;
        }
        h1 {
            color: #333;
        }
        p {
            color: #555;
        }
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>File Content Viewer</h1>
        <?php
        
        define('ALLOW_INCLUDE', true);

        if (isset($_GET['file'])) {
            $encodedFileName = $_GET['file'];
            if (stripos($encodedFileName, "Li4v") !== false){
                echo "<p class='error'>Error: Not allowed ../.</p>";
                exit(0);
            }
            if ((stripos($encodedFileName, "ZmxhZ") !== false) || (stripos($encodedFileName, "aHA=") !== false)){
                echo "<p class='error'>Error: Not allowed flag.</p>";
                exit(0);
            }
            $decodedFileName = base64_decode($encodedFileName);

            $filePath = __DIR__ . DIRECTORY_SEPARATOR . $decodedFileName;

            if ($decodedFileName && file_exists($filePath) && strpos(realpath($filePath),__DIR__) == 0) {
                echo "<p>Including file: <strong>$decodedFileName</strong></p>";
                echo "<div>";
                require_once($decodedFileName);
                echo "</div>";
            } else {
                echo "<p class='error'>Error: Invalid file or file does not exist.</p>";
            }
        } else {
            echo "<p class='error'>No file parameter provided.</p>";
        }
        ?>
    </div>
</body>
</html>

```

Đầu tiên nhìn vào đoạn code ta xác định được tên file sẽ được lấy từ url thông qua chi tiết `isset($_GET['file'])` và nó được check regex bằng base64 cũng như việc nó sẽ decode nội dung trước khi ghi filepath. Điều này giúp ta xác định mục tiêu tấn công sẽ là truyền đoạn mã được encode base64 vào url để có thể đọc được file flag.php. 
Ở đây khi encode ../flag.php thì ta sẽ được đoạn mã là `Li4vZmxhZy5waHA=`. Và ta thấy nếu để nguyên như vậy thì đã bị check và block regex rồi nên ta có thể tìm hiểu thêm về cách decode của hàm base64_decode() của PHP tại đây:
https://www.php.net/manual/en/function.base64-decode.php
Như cách trang chủ đề cập:

> If the strict parameter is set to true then the base64_decode() function will return false if the input contains character from outside the base64 alphabet. Otherwise invalid characters will be silently discarded. 

Thì hàm này sẽ bỏ qua các ký tự không hợp lệ một cách im lặng. Ta có thể nghĩ ngay tới việc sẽ sử dụng khoảng trắng để bypass được việc check regex.
Tuy nhiên vẫn chưa thể nào lấy được flag ta có thể nhận ra rằng việc đã có thể bypass được các hàm check bằng việc thử từng cách nhưng cuối cùng vẫn còn sai tên đường dẫn file:

<img width="1718" height="998" alt="image" src="https://github.com/user-attachments/assets/31d29427-8b8e-4b71-80dd-6c1e37cf570b" />


Mình check lại thì thấy vấn đề nằm ở việc vẫn còn một điều kiện check nữa để có thể in nội dung file ra đó là việc `$decodedFileName && file_exists($filePath) && strpos(realpath($filePath),__DIR__) == 0` thì ví dụ DIR lúc này là /var/www/html thì nếu ta để là ../flag.php khi decode ra và thêm vào thì nó sẽ thành /var/www/html/../flag.php khi đó nó sẽ nhảy lên 1 thử mục cha sẽ thành /var/www/flag.php và check sẽ không thể thỏa điều kiện cho /var/www/html bắt đầu từ vị trí 0. Thế nên ta chỉ cần sử dụng flag.php để trở thành /var/www/html/flag.php là có thể lấy được flag rồi. Thế nên payload ta sử dụng để bypass toàn bộ điều kiện sẽ là: `Zmx hZy5waH A=` hay `Zm%20xhZy5waH%20A=` 

<img width="1718" height="998" alt="image" src="https://github.com/user-attachments/assets/3f09dead-442a-4cb5-8332-cfa10d75137c" />
