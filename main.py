import heapq
from collections import defaultdict
import os
import tkinter as tk
from tkinter import filedialog


class HuffmanNode:
    def __init__(self, character=None, frequency=0):
        self.character = character
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency


def build_frequency_table(data):
    frequency_table = defaultdict(int)
    for char in data:
        frequency_table[char] += 1
    return frequency_table


def build_huffman_tree(frequency_table):
    heap = []
    for char, freq in frequency_table.items():
        node = HuffmanNode(char, freq)
        heapq.heappush(heap, node)

    if not heap:
        return None

    while len(heap) > 1:
        left_node = heapq.heappop(heap)
        right_node = heapq.heappop(heap)
        merged_node = HuffmanNode(frequency=left_node.frequency + right_node.frequency)
        merged_node.left = left_node
        merged_node.right = right_node
        heapq.heappush(heap, merged_node)

    return heap[0]


def build_encoding_table(huffman_tree):
    encoding_table = {}
    current_code = ""

    def traverse(node, code):
        if node.character is not None:
            encoding_table[node.character] = code
        else:
            traverse(node.left, code + "0")
            traverse(node.right, code + "1")

    traverse(huffman_tree, current_code)
    return encoding_table


def compress_file(file_path):
    if not os.path.isfile(file_path):
        return ""

    with open(file_path, "r", encoding="utf-8") as file:
        data = file.read()

    if not data:
        return ""

    frequency_table = build_frequency_table(data)
    huffman_tree = build_huffman_tree(frequency_table)

    if not huffman_tree:
        return ""

    encoding_table = build_encoding_table(huffman_tree)

    compressed_data = ""
    for char in data:
        compressed_data += encoding_table[char]

    compressed_file_path = file_path + ".compressed"

    with open(compressed_file_path, "w", encoding="utf-8") as compressed_file:

        for char, code in encoding_table.items():
            compressed_file.write(f"{char}:{code}\n")
        compressed_file.write("===\n")
        compressed_file.write(compressed_data)
    return "Операция выполнена успешно!"


def decompress_file(compressed_file_path):
    if not os.path.isfile(compressed_file_path):
        return "Такого файла нет, отправьте другой файл."

    with open(compressed_file_path, "r", encoding="utf-8") as compressed_file:

        encoding_table = {}
        line = compressed_file.readline().strip()
        while line != "===":
            parts = line.split(":")
            if len(parts) == 2:
                char, code = parts
                encoding_table[code] = char
            line = compressed_file.readline().strip()

        compressed_data = compressed_file.read()

    if not compressed_data:
        return ""

    decoded_data = ""
    current_code = ""
    for bit in compressed_data:
        current_code += bit
        if current_code in encoding_table:
            char = encoding_table[current_code]
            decoded_data += char
            current_code = ""

    decompressed_file_path = compressed_file_path + ".decompressed"

    with open(decompressed_file_path, "w", encoding="utf-8") as decompressed_file:
        decompressed_file.write(decoded_data)
    return "Операция выполнена успешно!"


class HuffmanEncoderDecoderApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Huffman Encoder/Decoder")
        self.window.configure(background="white")

        self.encode_button = tk.Button(self.window, text="Загрузить файл для кодирования", command=self.encode_file,
                                       bg="black", fg="white")
        self.encode_button.pack(pady=10)

        self.decode_button = tk.Button(self.window, text="Загрузить файл для раскодирования", command=self.decode_file,
                                       bg="black", fg="white")
        self.decode_button.pack(pady=10)

        self.start_button = tk.Button(self.window, text="Запустить программу", command=self.run_program, bg="green",
                                      fg="white")
        self.start_button.pack(pady=10)

    def encode_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            compression_result = compress_file(file_path)
            print(compression_result)

    def decode_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.compressed")])
        if file_path:
            decompression_result = decompress_file(file_path)
            print(decompression_result)

    def run_program(self):
        pass

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = HuffmanEncoderDecoderApp()
    app.run()
