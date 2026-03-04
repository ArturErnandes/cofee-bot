#include "classes.h"

int main() {
    FooEngine engine;
    FooCmdReceiver receiver;
    ControlSystem system(&receiver, &engine);

    system.run();

    return 0;
}