#include <iostream>
#include <unordered_set>
#include <vector>
#include <string>
#include <random>
#include <sstream>
#include <iomanip>
#include <memory>

#ifdef __APPLE__
#include <CommonCrypto/CommonDigest.h>
#define SHA256_DIGEST_LENGTH CC_SHA256_DIGEST_LENGTH
#else
#include <openssl/sha.h>
#endif

class MyObj {
public:
    std::string name;
    MyObj(const std::string& n) : name(n) {}
    
    friend std::ostream& operator<<(std::ostream& os, const MyObj& obj) {
        os << obj.name;
        return os;
    }
};

// Custom hash function for unique_ptr<MyObj>
namespace std {
    template<>
    struct hash<unique_ptr<MyObj>> {
        size_t operator()(const unique_ptr<MyObj>& p) const {
            return hash<MyObj*>()(p.get());
        }
    };
}

// Custom equality operator for unique_ptr<MyObj>
bool operator==(const std::unique_ptr<MyObj>& lhs, const std::unique_ptr<MyObj>& rhs) {
    return lhs.get() == rhs.get();
}

std::string sha256(const std::string& str) {
    unsigned char hash[SHA256_DIGEST_LENGTH];
#ifdef __APPLE__
    CC_SHA256_CTX sha256;
    CC_SHA256_Init(&sha256);
    CC_SHA256_Update(&sha256, str.c_str(), str.size());
    CC_SHA256_Final(hash, &sha256);
#else
    SHA256_CTX sha256;
    SHA256_Init(&sha256);
    SHA256_Update(&sha256, str.c_str(), str.size());
    SHA256_Final(hash, &sha256);
#endif

    std::stringstream ss;
    for(int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
        ss << std::hex << std::setw(2) << std::setfill('0') << (int)hash[i];
    }
    return ss.str();
}

std::vector<std::string> demonstrate_address_randomization(int n) {
    std::vector<std::unique_ptr<MyObj>> objs;
    std::unordered_set<std::unique_ptr<MyObj>> obj_set;
    
    // Create objects
    for (int i = 0; i < n; i++) {
        auto obj = std::make_unique<MyObj>("object_" + std::to_string(i));
        obj_set.insert(std::move(obj));
    }
    
    // Convert set to vector of names
    std::vector<std::string> result;
    for (const auto& obj : obj_set) {
        result.push_back(obj->name);
    }
    
    return result;
    // No cleanup needed - unique_ptr handles deletion automatically
}

void test_setmeup() {
    std::unordered_set<std::string> order_hist;
    const int num_lists = 1000;
    const int length = 30;
    
    for (int i = 0; i < num_lists; i++) {
        auto x = demonstrate_address_randomization(length);
        
        // Create a string representation of the vector for hashing
        std::string to_hash;
        for (const auto& name : x) {
            to_hash += name;
        }
        
        order_hist.insert(sha256(to_hash));
    }
    
    // Assert equivalent
    if (order_hist.size() == num_lists) {
        std::cout << "Test passed: All iterations produced different orders\n";
    } else {
        std::cout << "Test failed: Some iterations produced the same order\n";
        std::cout << "Unique orders: " << order_hist.size() << " out of " << num_lists << "\n";
    }
}

int main() {
    test_setmeup();
    return 0;
}