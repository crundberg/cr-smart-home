#include <nan.h>
#include "RCSwitchNode.h"

void InitAll(v8::Local<v8::Object> exports) {
  RCSwitchNode::Init(exports);
}

NODE_MODULE(rcswitch, InitAll)