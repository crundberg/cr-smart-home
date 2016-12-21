#ifndef RCSWITCHNODE_H
#define RCSWITCHNODE_H

#include <nan.h>

#include "../externals/rcswitch-pi/RCSwitch.h"

class RCSwitchNode : public Nan::ObjectWrap {
 public:
  static void Init(v8::Local<v8::Object> exports);

 private:
  RCSwitch rcswitch;
  static Nan::Persistent<v8::Function> constructor;
  explicit RCSwitchNode();
  ~RCSwitchNode();
  
  static void SwitchOp(const Nan::FunctionCallbackInfo<v8::Value>& info, bool switchOn);
  #define switchOp2(p1, p2) { if(switchOn) thiz->rcswitch.switchOn((p1), (p2)); else thiz->rcswitch.switchOff((p1), (p2)); }
  #define switchOp3(p1, p2, p3) { if(switchOn) thiz->rcswitch.switchOn((p1), (p2), (p3)); else thiz->rcswitch.switchOff((p1), (p2), (p3)); }
  static void New(const Nan::FunctionCallbackInfo<v8::Value>& info);
  static void Send(const Nan::FunctionCallbackInfo<v8::Value>& info);
  static void EnableTransmit(const Nan::FunctionCallbackInfo<v8::Value>& info);
  static void DisableTransmit(const Nan::FunctionCallbackInfo<v8::Value>& info);
  static void SetPulseLength(const Nan::FunctionCallbackInfo<v8::Value>& info);
  static void SetRepeatTransmit(const Nan::FunctionCallbackInfo<v8::Value>& info);
  static void SwitchOn(const Nan::FunctionCallbackInfo<v8::Value>& info);
  static void SwitchOff(const Nan::FunctionCallbackInfo<v8::Value>& info);
  
  static void SetProtocol(v8::Local<v8::String> property, v8::Local<v8::Value> value, const Nan::PropertyCallbackInfo<v8::Value>& info);
  static void GetProtocol(v8::Local<v8::String> property, const Nan::PropertyCallbackInfo<v8::Value>& info);
};

#endif
