# Learning Week ROS 2 Publisher & Subscriber

Membuat sistem komunikasi sederhana di ROS 2 menggunakan:

* Publisher (Talker)
* Subscriber (Listener)
* Publisher akan mengirim pesan setiap 1 detik, dan Subscriber akan menerima serta menampilkannya.

---

# STEP 1 — Buat Workspace

Buat folder projek :

```bash
mkdir -p ros2_ws/src
cd ros2_ws
```

---

# STEP 2 — Source ROS 2

Pastikan ROS 2 sudah terinstall :

```bash
source /opt/ros/jazzy/setup.bash
```

Cek:

```bash
which ros2
```

---

# STEP 3 — Buat Package Python

Masuk ke folder src:

```bash
cd src
```

Buat package:

```bash
ros2 pkg create --build-type ament_python py_pubsub
```

---

# STEP 4 — Buat Publisher

Masuk ke folder python:

```bash
cd py_pubsub/py_pubsub
```

Buat file:

```bash
nano publisher.py
```

Isi dengan:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Publisher(Node):

    def __init__(self):
        super().__init__('publisher_node')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.count = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello World {self.count}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: {msg.data}')
        self.count += 1


def main(args=None):
    rclpy.init(args=args)
    node = Publisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## Penjelasan STEP 4 (Publisher)

Bagian import:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
```

* `rclpy` adalah library utama ROS 2 untuk Python.
* `Node` digunakan sebagai class dasar untuk membuat node.
* `String` adalah tipe pesan standar untuk mengirim data teks.

Class Publisher:

```python
class Publisher(Node):
```

Node di ROS 2 adalah unit eksekusi program. Publisher merupakan node yang bertugas mengirim data ke sebuah topic.

Constructor:

```python
super().__init__('publisher_node')
```

Memberikan nama node yaitu `publisher_node`. Nama ini akan terlihat jika menjalankan perintah `ros2 node list`.

Membuat publisher:

```python
self.publisher_ = self.create_publisher(String, 'topic', 10)
```

Penjelasan:

* `String` → tipe pesan yang dikirim.
* `'topic'` → nama topic komunikasi.
* `10` → ukuran queue (jumlah pesan yang bisa ditampung sementara).

Membuat timer:

```python
self.timer = self.create_timer(1.0, self.timer_callback)
```

Timer akan memanggil fungsi `timer_callback` setiap 1 detik. Artinya publisher mengirim pesan secara periodik setiap 1 detik.

Counter:

```python
self.count = 0
```

Digunakan untuk menghitung jumlah pesan yang telah dikirim.

Fungsi callback:

```python
def timer_callback(self):
```

Fungsi ini otomatis dijalankan setiap 1 detik oleh timer.

Membuat pesan:

```python
msg = String()
msg.data = f'Hello World {self.count}'
```

Membuat objek pesan bertipe String lalu mengisi data teks.

Mengirim pesan:

```python
self.publisher_.publish(msg)
```

Pesan dikirim ke topic `'topic'`.

Menampilkan log:

```python
self.get_logger().info(f'Publishing: {msg.data}')
```

Menampilkan pesan di terminal untuk memastikan data terkirim.

Menambah counter:

```python
self.count += 1
```

Agar angka bertambah setiap kali pesan dikirim.

Bagian main:

```python
rclpy.init(args=args)
```

Menginisialisasi sistem ROS 2.

```python
node = Publisher()
```

Membuat instance node Publisher.

```python
rclpy.spin(node)
```

Menjalankan node agar terus aktif dan memproses event.

```python
node.destroy_node()
rclpy.shutdown()
```

Membersihkan node dan mematikan ROS 2 dengan aman.

---

# STEP 5 — Buat Subscriber

```bash
nano subscriber.py
```

Isi dengan:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Subscriber(Node):

    def __init__(self):
        super().__init__('subscriber_node')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10
        )

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    node = Subscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## Penjelasan STEP 5 (Subscriber)

Bagian import sama seperti publisher karena tetap menggunakan `rclpy`, `Node`, dan `String`.

Class Subscriber:

```python
class Subscriber(Node):
```

Subscriber adalah node yang bertugas menerima data dari topic.

Constructor:

```python
super().__init__('subscriber_node')
```

Memberikan nama node yaitu `subscriber_node`.

Membuat subscription:

```python
self.subscription = self.create_subscription(
    String,
    'topic',
    self.listener_callback,
    10
)
```

Penjelasan:

* `String` → tipe pesan yang diterima.
* `'topic'` → harus sama dengan topic publisher.
* `self.listener_callback` → fungsi yang dijalankan saat pesan diterima.
* `10` → ukuran queue.

Fungsi callback:

```python
def listener_callback(self, msg):
```

Fungsi ini otomatis dijalankan setiap kali ada pesan baru dari topic.

Menampilkan pesan:

```python
self.get_logger().info(f'I heard: {msg.data}')
```

Menampilkan isi pesan yang diterima di terminal.

Bagian main sama seperti publisher:

* Inisialisasi ROS 2
* Membuat node Subscriber
* Menjalankan node dengan `spin()`
* Shutdown dengan aman

---

# STEP 6 — Edit package.xml

Tambahkan:

```xml
<exec_depend>rclpy</exec_depend>
<exec_depend>std_msgs</exec_depend>
```

---

# STEP 7 — Edit setup.py

```python
entry_points={
    'console_scripts': [
        'talker = py_pubsub.publisher:main',
        'listener = py_pubsub.subscriber:main',
    ],
},
```

---

# STEP 8 — Build

```bash
cd ../../
colcon build
```

---

# STEP 9 — Jalankan Publisher

```bash
source install/setup.bash
ros2 run py_pubsub talker
```

Output:

![Gambar Publisher](asset/publisher.png)

---

# STEP 10 — Jalankan Subscriber

Terminal 2:

```bash
cd ros2_ws
source install/setup.bash
ros2 run py_pubsub listener
```

Output:

![Gambar Subscriber](asset/subscriber.png)

---

# TUGAS KINGGGGG
Berdasarkan project yang telah dibuat, lakukan pengembangan sistem menjadi:

### 2 Publisher dan 1 Subscriber

---

## Ketentuan

###  Publisher 1

* Topic: `/topic1`
* Publish setiap 1 detik
* Format pesan:

```
From Publisher 1: <counter>
```

### Publisher 2

* Topic: `/topic2`
* Publish setiap 2 detik
* Format pesan:

```
From Publisher 2: <counter>
```

### Subscriber

* Harus subscribe ke:

  * `/topic1`
  * `/topic2`
* Gunakan 2 callback berbeda
* Output harus dibedakan:

Contoh:

```
[TOPIC1] From Publisher 1: 0
[TOPIC2] From Publisher 2: 0
[TOPIC1] From Publisher 1: 1
```

# Refrensi
https://docs.ros.org/en/foxy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html
