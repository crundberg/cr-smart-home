{
  'targets': [
    {
      'target_name': 'rcswitch-gpiomem',
      'sources': [ 'src/rcswitch.cpp', 'src/RCSwitchNode.cpp', 'externals/rcswitch-pi/RCSwitch.cpp' ],
      'include_dirs': [ '/usr/local/include', "<!(node -e \"require('nan')\")" ],
      'ldflags': [ '-lwiringPi' ]
    }
  ]
}
