# Copyright 2012 (c) Kyan <kyan.ql.he@gmail.com>
{
  'targets': [
    {
      # Force use_system_zlib = 1.
      'target_name': 'zlib',
      'type': 'none',

      'conditions': [
        ['OS == "ios"', {
          'link_settings': {
            'libraries': [
              '$(SDKROOT)/usr/lib/libz.dylib',
            ],
          }
        }, { # OS != 'ios'
          'link_settings': {
            'libraries': [
              '-lz',
            ],
          }
        }]
      ],
    }
  ],
}
