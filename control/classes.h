#ifndef CLASSES_H
#define CLASSES_H

#include <iostream>
#include <string>
#include <thread>
#include <chrono>

using namespace std;

class AEngine {
public:
    virtual void forward(int time_ms) = 0;
    virtual void right(int time_ms) = 0;
    virtual void left(int time_ms) = 0;
    virtual void stop() = 0;
    virtual ~AEngine() = default;
};

class FooEngine : public AEngine {
public:
    void forward(int time_ms) override {
        cout << "move forward " << time_ms << " ms" << endl;
        this_thread::sleep_for(chrono::milliseconds(time_ms));
        stop();
    }

    void right(int time_ms) override {
        cout << "move right " << time_ms << " ms" << endl;
        this_thread::sleep_for(chrono::milliseconds(time_ms));
        stop();
    }

    void left(int time_ms) override {
        cout << "move left " << time_ms << " ms" << endl;
        this_thread::sleep_for(chrono::milliseconds(time_ms));
        stop();
    }

    void stop() override {
        cout << "stop" << endl;
    }
};

class ACmdReceiver {
public:
    virtual string receive() = 0;
    virtual ~ACmdReceiver() = default;
};

class FooCmdReceiver : public ACmdReceiver {
public:
    string receive() override {
        string cmd;
        cin >> cmd;
        return cmd;
    }
};

class ControlSystem {
private:
    ACmdReceiver* receiver;
    AEngine* engine;

public:
    ControlSystem(ACmdReceiver* r, AEngine* e) {
        receiver = r;
        engine = e;
    }

    void run() {
        string cmd;

        cmd = receiver->receive();

        if (cmd == "stop") {
            engine->stop();
        }
        else {
            int time_ms;
            cin >> time_ms;

            if (cmd == "forward") {
                engine->forward(time_ms);
            }
            else if (cmd == "right") {
                engine->right(time_ms);
            }
            else if (cmd == "left") {
                engine->left(time_ms);
            }
        }
    }
};
#endif