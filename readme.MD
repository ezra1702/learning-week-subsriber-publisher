# Learning Week ROS 2 Publisher & Subscriber

Dokumentasi ini menjelaskan pembuatan sistem komunikasi sederhana menggunakan arsitektur Publisher–Subscriber pada ROS 2 dengan bahasa Python.

Sistem terdiri dari:

* Publisher (Talker)
* Subscriber (Listener)

Publisher mengirimkan pesan setiap 1 detik ke sebuah topic, dan Subscriber menerima serta menampilkan pesan tersebut.

---

# Konsep Dasar

## Node

Node adalah unit eksekusi dalam ROS 2. Setiap program yang berjalan di dalam ROS 2 disebut node. Node dapat berperan sebagai publisher, subscriber, service server, service client, dan lainnya.

## Topic

Topic adalah saluran komunikasi yang digunakan oleh publisher dan subscriber untuk bertukar data. Publisher mengirim pesan ke topic, dan subscriber menerima pesan dari topic tersebut.

## Message

Message adalah tipe data yang dikirim melalui topic. Dalam contoh ini digunakan tipe `String` dari package `std_msgs`.

## Publisher–Subscriber

Publisher mengirim data ke topic tanpa mengetahui siapa yang menerima. Subscriber mendengarkan topic tanpa mengetahui siapa yang mengirim. Sistem ini bersifat asynchronous dan loosely coupled.

---

# STEP 1 — Membuat Workspace

Workspace adalah direktori kerja tempat seluruh package ROS 2 disimpan dan dibangun.

```bash
mkdir -p ros2_ws/src
cd ros2_ws
```

Struktur workspace:

```
ros2_ws/
 ├── src/
 ├── build/
 ├── install/
 └── log/
```

Folder `src` digunakan untuk menyimpan package.

---

# STEP 2 — Source ROS 2

Sebelum menggunakan ROS 2, environment harus diaktifkan.

```bash
source /opt/ros/jazzy/setup.bash
```

Perintah ini mengatur environment variable agar sistem mengenali perintah `ros2`.

Verifikasi instalasi:

```bash
which ros2
```

Jika berhasil, sistem akan menampilkan lokasi executable ROS 2.

---

# STEP 3 — Membuat Package Python

Masuk ke folder `src`:

```bash
cd src
```

Buat package:

```bash
ros2 pkg create --build-type ament_python py_pubsub
```

Penjelasan:

* `ros2 pkg create` membuat package baru.
* `--build-type ament_python` digunakan untuk package berbasis Python.
* `py_pubsub` adalah nama package.

Struktur yang dihasilkan:

```
py_pubsub/
 ├── package.xml
 ├── setup.py
 ├── py_pubsub/
 └── resource/
```

---

# STEP 4 — Membuat Publisher

Masuk ke folder Python:

```bash
cd py_pubsub/py_pubsub
```

Buat file:

```bash
nano publisher.py
```

Isi file:

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

## Penjelasan Publisher

### Import

* `rclpy` adalah client library ROS 2 untuk Python.
* `Node` adalah class dasar untuk membuat node.
* `String` adalah tipe pesan teks dari `std_msgs`.

### Class Publisher

```python
class Publisher(Node):
```

Publisher merupakan turunan dari class `Node`. Ini berarti Publisher adalah sebuah node dalam sistem ROS 2.

### Constructor

```python
super().__init__('publisher_node')
```

Memberikan nama node yaitu `publisher_node`.

### Membuat Publisher

```python
self.publisher_ = self.create_publisher(String, 'topic', 10)
```

Parameter:

* `String` adalah tipe pesan.
* `'topic'` adalah nama topic komunikasi.
* `10` adalah ukuran queue untuk menyimpan pesan sementara.

### Timer

```python
self.timer = self.create_timer(1.0, self.timer_callback)
```

Timer memanggil fungsi `timer_callback` setiap 1 detik.

### Counter

```python
self.count = 0
```

Digunakan untuk menghitung jumlah pesan yang telah dikirim.

### Fungsi Callback

Fungsi `timer_callback` dijalankan secara periodik oleh timer.

Langkah di dalamnya:

1. Membuat objek pesan.
2. Mengisi data pesan.
3. Mengirim pesan ke topic.
4. Menampilkan log ke terminal.
5. Menambah nilai counter.

### Fungsi main

* `rclpy.init()` menginisialisasi sistem ROS.
* Membuat instance node Publisher.
* `rclpy.spin()` menjaga node tetap aktif.
* `destroy_node()` dan `shutdown()` membersihkan resource.

---

# STEP 5 — Membuat Subscriber

Buat file:

```bash
nano subscriber.py
```

Isi file:

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

## Penjelasan Subscriber

### Class Subscriber

Subscriber adalah node yang menerima pesan dari topic.

### Constructor

```python
super().__init__('subscriber_node')
```

Memberikan nama node `subscriber_node`.

### Membuat Subscription

```python
self.subscription = self.create_subscription(
    String,
    'topic',
    self.listener_callback,
    10
)
```

Parameter:

* `String` adalah tipe pesan.
* `'topic'` harus sama dengan publisher.
* `self.listener_callback` adalah fungsi yang dipanggil saat pesan diterima.
* `10` adalah ukuran queue.

### Callback Function

Fungsi ini otomatis dijalankan setiap ada pesan masuk.

```python
self.get_logger().info(f'I heard: {msg.data}')
```

Menampilkan isi pesan yang diterima.

### Fungsi main

Struktur sama seperti publisher:

* Inisialisasi ROS
* Membuat node
* Spin
* Shutdown

---

# STEP 6 — Edit package.xml

Tambahkan dependensi:

```xml
<exec_depend>rclpy</exec_depend>
<exec_depend>std_msgs</exec_depend>
```

Penjelasan:

* `rclpy` diperlukan untuk menjalankan node Python.
* `std_msgs` diperlukan untuk menggunakan tipe pesan `String`.

---

# STEP 7 — Edit setup.py

Tambahkan entry point:

```python
entry_points={
    'console_scripts': [
        'talker = py_pubsub.publisher:main',
        'listener = py_pubsub.subscriber:main',
    ],
},
```

Penjelasan:

* `talker` adalah nama executable untuk publisher.
* `listener` adalah nama executable untuk subscriber.
* `py_pubsub.publisher:main` menunjuk ke fungsi `main()` di file publisher.py.

---

# STEP 8 — Build

Kembali ke root workspace:

```bash
cd ../../
colcon build
```

Proses ini akan:

* Mengompilasi package
* Membuat folder build
* Membuat folder install
* Membuat folder log

---

# STEP 9 — Menjalankan Publisher

```bash
source install/setup.bash
ros2 run py_pubsub talker
```

Publisher akan mengirim pesan setiap 1 detik.


Output :
![Publisher](assets/publisher.png)

---


# STEP 10 — Menjalankan Subscriber

Terminal baru:

```bash
cd ros2_ws
source install/setup.bash
ros2 run py_pubsub listener
```

Subscriber akan menerima dan menampilkan pesan dari topic.

Output :
![Subscriber](assets/subscriber.png)

---

# Alur Komunikasi Sistem

1. Publisher membuat pesan bertipe String.
2. Pesan dikirim ke topic bernama `topic`.
3. Subscriber yang mendengarkan topic tersebut menerima pesan.
4. Callback subscriber dipanggil.
5. Pesan ditampilkan di terminal.

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
# Referensi

Tutorial resmi ROS 2:

[https://docs.ros.org/en/foxy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html](https://docs.ros.org/en/foxy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html)

---