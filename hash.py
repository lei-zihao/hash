import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size  # 初始化哈希表
        self.DELETED = "DELETED"  # 特殊标记，表示已删除的位置

    def hash_function(self, key):
        return key % self.size  # 除留余数法构造哈希函数

    def linear_probing(self, key, index):
        return (index + 1) % self.size  # 线性探测再散列处理冲突


    # 将每个i与self.table[i]组成一个元组，然后将这些元组放在一个列表中返回。
    def display(self):
        return [(i, self.table[i]) for i in range(self.size)]

    def search(self, key):
        index = self.hash_function(key)
        start_index = index
        while self.table[index] is not None:
            if self.table[index] == key:
                return index
            index = self.linear_probing(key, index)
            if index == start_index:
                break
        return -1

    def insert(self, key):
        index = self.hash_function(key)
        if self.table[index] is None or self.table[index] == self.DELETED:
            self.table[index] = key
            return True
        else:
            start_index = index
            index = self.linear_probing(key, index)
            while index != start_index and self.table[index] is not None and self.table[index] != self.DELETED:
                index = self.linear_probing(key, index)
            if index != start_index:
                self.table[index] = key
                return True
            else:
                return False

    def delete(self, key):
        index = self.hash_function(key)
        start_index = index
        while self.table[index] is not None:
            if self.table[index] == key:
                self.table[index] = self.DELETED
                return True
            index = self.linear_probing(key, index)
            if index == start_index:
                break
        return False

# GUI部分
class HashTableGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("哈希表管理系统")

        self.size_label = tk.Label(root, text="哈希表大小:")
        self.size_label.pack()

        self.size_entry = tk.Entry(root)
        self.size_entry.pack()

        self.create_button = tk.Button(root, text="创建哈希表", command=self.create_hash_table)
        self.create_button.pack()

        self.operation_frame = tk.Frame(root)
        self.operation_frame.pack()

        self.key_label = tk.Label(self.operation_frame, text="元素:")
        self.key_label.grid(row=0, column=0)

        self.key_entry = tk.Entry(self.operation_frame)
        self.key_entry.grid(row=0, column=1)

        self.insert_button = tk.Button(self.operation_frame, text="插入", command=self.insert_key)
        self.insert_button.grid(row=1, column=0)

        self.search_button = tk.Button(self.operation_frame, text="查找", command=self.search_key)
        self.search_button.grid(row=1, column=1)

        self.delete_button = tk.Button(self.operation_frame, text="删除", command=self.delete_key)
        self.delete_button.grid(row=1, column=2)

        self.hash_table_view = ttk.Treeview(root, columns=("Index", "Value"), show="headings")
        self.hash_table_view.heading("Index", text="索引")
        self.hash_table_view.heading("Value", text="值")
        self.hash_table_view.pack()

        self.hash_table = None

    def create_hash_table(self):
        try:
            size = int(self.size_entry.get())
            self.hash_table = HashTable(size)
            self.update_display()
            messagebox.showinfo("成功", "哈希表创建成功!")
        except ValueError:
            messagebox.showerror("错误", "请输入有效的整数大小!")

    def insert_key(self):
        if self.hash_table is None:
            messagebox.showerror("错误", "请先创建哈希表!")
            return
        try:
            key = int(self.key_entry.get())
            if self.hash_table.insert(key):
                self.update_display()
                messagebox.showinfo("成功", "元素插入成功!")
            else:
                messagebox.showerror("错误", "哈希表已满，插入失败!")
        except ValueError:
            messagebox.showerror("错误", "请输入有效的整数元素!")

    def search_key(self):
        if self.hash_table is None:
            messagebox.showerror("错误", "请先创建哈希表!")
            return
        try:
            key = int(self.key_entry.get())
            index = self.hash_table.search(key)
            if index != -1:
                messagebox.showinfo("成功", f"元素 {key} 在索引 {index} 处找到。")
            else:
                messagebox.showerror("错误", "元素未找到!")
        except ValueError:
            messagebox.showerror("错误", "请输入有效的整数元素!")

    def delete_key(self):
        if self.hash_table is None:
            messagebox.showerror("错误", "请先创建哈希表!")
            return
        try:
            key = int(self.key_entry.get())
            if self.hash_table.delete(key):
                self.update_display()
                messagebox.showinfo("成功", "元素删除成功!")
            else:
                messagebox.showerror("错误", "元素未找到，删除失败!")
        except ValueError:
            messagebox.showerror("错误", "请输入有效的整数元素!")

    def update_display(self):
        if self.hash_table is not None:
            for i in self.hash_table_view.get_children():
                self.hash_table_view.delete(i)
            for index, value in self.hash_table.display():
                if value is None:
                    value_str = "空"
                elif value == self.hash_table.DELETED:
                    value_str = "已删除"
                else:
                    value_str = str(value)
                self.hash_table_view.insert("", "end", values=(index, value_str))

if __name__ == "__main__":
    root = tk.Tk()
    app = HashTableGUI(root)
    root.mainloop()
