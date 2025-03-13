#include <iostream>
#include <unordered_map>

class MyObject {
public:
    int value;
    MyObject(int val) : value(val) {}
    // Make operator<< a friend function
    friend std::ostream& operator<<(std::ostream& os, const MyObject& obj);
};

// Define operator<< outside the class
std::ostream& operator<<(std::ostream& os, const MyObject& obj) {
    os << obj.value;
    return os;
}

int main() {
  const auto LIST_LENGTH = 100;
  // Create an unordered_map with MyObject pointers as keys
  std::unordered_map<MyObject*, int> myMap;
  
  for (auto i = 0; i < LIST_LENGTH; i++) {
    auto obj = new MyObject(i);
    myMap[obj] = 1;
  }
  
  // Correct iteration over map pairs
  for (const auto& pair : myMap) {
    std::cout << *(pair.first) << std::endl;
  }
  
  return 0;
}
