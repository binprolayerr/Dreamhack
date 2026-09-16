https://dreamhack.io/wargame/challenges/1367

Bài này ta được cho đoạn mã như sau:

```php
<html>
<head>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">
    <title>PHParse</title>
</head>
<body>


    <!-- php code -->
    <?php
     $url = $_SERVER['REQUEST_URI'];
     $host = parse_url($url,PHP_URL_HOST);
     $path = parse_url($url,PHP_URL_PATH);
     $query = parse_url($url,PHP_URL_QUERY);
     echo "<div><h1> host: $host <br> path: $path <br> query: $query<br></h1></div>";

     if(preg_match("/flag.php/i", $path)){
        echo "<div><h1>NO....</h1></div>";
     }
     else echo "<div><h1>Cannot access flag.php: $path </h1></div> ";
    ?> 

<style type="text/css">
        body {
            margin: 1em;
        }
        div {
            margin: 0 5px 0 0;
            padding: 0.1em;
            border: 2px solid silver;
            border-radius: 7px;
        }

</style>
</body>
</html>
```

Trong code này ta có thể nhận thấy tác giả sử dụng parse_url() để đọc từ url lấy host path và query. Để hiểu về cách hoạt động của parse url bạn có thể search tại đây:

https://www.php.net/parse-url

Từ đây ta có thể thấy nếu ta đưa vào /flag.php thì nó sẽ nhận:

```php
host = NULL
path = /flag.php 
query = NULL 
```

Lúc này thì ngay lập tức sẽ bị match với chuỗi cấm ngay và xuất ra NO....

Thế nên ta suy nghĩ một hướng tiếp cận khác để đánh lừa hàm parse_url(). Ta có thể nghĩ đến việc sẽ sử dụng //flag.php vì parse_url() sẽ nhận diện // thành network-path thế nên lúc này:

```php
host = flag.php
path = NULL 
query = NULL 
```

Cuối cùng ta nhận được flag:

<img width="1718" height="998" alt="Screenshot_2026-09-16_10_18_55" src="https://github.com/user-attachments/assets/fc1f1ee5-9a41-4212-b24f-6bc6ef991dbb" />
