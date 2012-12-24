# Copyright 2012 (c) Kyan <kyan.ql.he@gmail.com>
{
  'variables': {
    'use_system_minizip%': 0,
    'os_bsd%': 0,
  },

  'targets': [
    {
      # Force use_system_zlib = 1.
      'target_name': 'zlib',
      'type': 'none',

      'direct_dependent_settings': {
        'defines': [
          'USE_SYSTEM_ZLIB', # For use with with minizip.
        ],
      },

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
        }],

        ['OS == "android"', {
          # TODO(kyan): gyp does not support none type for Android NDK.
          'type': 'static_library',
        }],
      ],
    },

    {
      'target_name': 'minizip',
      'type': 'static_library',
      'dependencies': [
        'zlib',
      ],
      'conditions': [
        ['use_system_minizip == 0', {
          'sources': [
            'contrib/minizip/ioapi.c',
            'contrib/minizip/ioapi.h',
            'contrib/minizip/iowin32.c',
            'contrib/minizip/iowin32.h',
            'contrib/minizip/unzip.c',
            'contrib/minizip/unzip.h',
            'contrib/minizip/zip.c',
            'contrib/minizip/zip.h',
          ],
          'include_dirs': [
            '.',
            '../..',
          ],
          'direct_dependent_settings': {
            'include_dirs': [
              '.',
            ],
          },
          'conditions': [
            ['OS != "win"', {
              'sources!': [
                'contrib/minizip/iowin32.c'
              ],
            }],
          ],
        }, { # use_system_minizip != 0
          'direct_dependent_settings': {
            'defines': [
              'USE_SYSTEM_MINIZIP',
            ],
          },
          'defines': [
            'USE_SYSTEM_MINIZIP',
          ],
          'link_settings': {
            'libraries': [
              '-lminizip',
            ],
          },
        }], # use_system_minizip

        ['OS=="mac" or OS=="ios" or os_bsd==1 or OS=="android"', {
          # Mac, Android and the BSDs don't have fopen64, ftello64, or
          # fseeko64. We use fopen, ftell, and fseek instead on these
          # systems.
          'defines': [
            'USE_FILE32API'
          ],
        }],

        ['clang==1', {
          'xcode_settings': {
            'WARNING_CFLAGS': [
              # zlib uses `if ((a == b))` for some reason.
              '-Wno-parentheses-equality',
            ],
          },
          'cflags': [
            '-Wno-parentheses-equality',
          ],
        }],
      ],
    }
  ],
}
