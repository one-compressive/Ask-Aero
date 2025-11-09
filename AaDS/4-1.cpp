/*Напишите программу, которая использует кучу для слияния K отсортированных массивов суммарной длиной N.

Требования:

Время работы O(N * logK)
Куча должна быть реализована в виде шаблонного класса.
Решение должно поддерживать передачу функции сравнения снаружи.
Куча должна быть динамической.*/
#include <iostream>
#include <functional>
#include <utility>

template <typename T, bool(*)(const T&, const T&)>
class Heap {
 public:
  explicit Heap(size_t capacity = 16)
      : size_(0), capacity_(capacity), data_(new T[capacity]) {}

  ~Heap() {
    delete[] data_;
  }

  Heap(const Heap& other)
      : size_(other.size_), capacity_(other.capacity_), data_(new T[other.capacity_]) {
    for (size_t i = 0; i < size_; ++i) {
      data_[i] = other.data_[i];
    }
  }

  Heap& operator=(const Heap& other) {
    if (this == &other) return *this;
    delete[] data_;
    capacity_ = other.capacity_;
    size_ = other.size_;
    data_ = new T[capacity_];
    for (size_t i = 0; i < size_; ++i) {
      data_[i] = other.data_[i];
    }
    return *this;
  }

  bool IsEmpty() const { return size_ == 0; }
  size_t Size() const { return size_; }

  const T& PeekRoot() const {
    return data_[0];
  }

  void Insert(const T& value) {
    if (size_ == capacity_) {
      Resize(capacity_ * 2);
    }
    data_[size_] = value;
    SiftUp(size_);
    ++size_;
  }

  T ExtractRoot() {
    T result = data_[0];
    data_[0] = data_[size_ - 1];
    --size_;
    SiftDown(0);
    return result;
  }

 private:
  T* data_;
  size_t size_;
  size_t capacity_;

  void Resize(size_t new_capacity) {
    T* new_data = new T[new_capacity];
    for (size_t i = 0; i < size_; ++i) {
      new_data[i] = data_[i];
    }
    delete[] data_;
    data_ = new_data;
    capacity_ = new_capacity;
  }

  void SiftUp(size_t index) {
    while (index > 0) {
      size_t parent = (index - 1) / 2;
      if (!comp(data_[index], data_[parent])) {
        break;
      }
      std::swap(data_[index], data_[parent]);
      index = parent;
    }
  }

  void SiftDown(size_t index) {
    while (true) {
      size_t left = 2 * index + 1;
      size_t right = 2 * index + 2;
      size_t smallest = index;

      if (left < size_ && comp(data_[left], data_[smallest])) {
        smallest = left;
      }
      if (right < size_ && comp(data_[right], data_[smallest])) {
        smallest = right;
      }
      if (smallest == index) {
        break;
      }
      std::swap(data_[index], data_[smallest]);
      index = smallest;
    }
  }
};

struct HeapNode {
    int value;
    size_t arr_idx;
    size_t elem_idx;
    HeapNode() : value(0), arr_idx(0), elem_idx(0) {}
    HeapNode(int v, size_t a, size_t e) : value(v), arr_idx(a), elem_idx(e) {}
};

bool comp(const HeapNode &a, const HeapNode &b) {
    return (a.value < b.value);
}

int* MergeArrays(int** arrs, const size_t* sizes, size_t k, size_t n) {
    Heap<HeapNode, comp> heap;

    for (size_t i=0; i<k; ++i) {
        heap.Insert(HeapNode(arrs[i][0], i, 0));
    }

    size_t index=0;
    int* result = new int[n];

    while (!heap.IsEmpty()) {
        HeapNode node=heap.ExtractRoot();
        result[index++]=node.value;

        if (node.elem_idx + 1 < sizes[node.arr_idx]) {
            heap.Insert(HeapNode(arrs[node.arr_idx][node.elem_idx+1], node.arr_idx, node.elem_idx+1));
        }
    }
    return result;
}

int main() {
    size_t k, n=0;
    std::cin >> k;
    size_t* sizes = new size_t[k];
    int** arrs = new int*[k];

    for (size_t i=0; i<k; ++i) {
        std::cin >> sizes[i];
        n+=sizes[i];
        arrs[i] = new int[sizes[i]];
        for (size_t j=0; j<sizes[i]; ++j) {
            std::cin >> arrs[i][j];
        }
    }

    int* result=MergeArrays(arrs, sizes, k, n);
    for (int i=0; i<n; ++i) {
        std::cout << result[i] << " ";
    }

    for (size_t i = 0; i < k; ++i) delete[] arrs[i];
  delete[] arrs;
  delete[] sizes;
  delete[] result;
}

//сложность по времени: O(N log K), по памяти: O(K)+O(N)
