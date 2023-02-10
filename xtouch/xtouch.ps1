#!/usr/bin/env pwsh

# A powershell script to recursively set the last access time
# of all files in a directory tree to the current date and
# time.

function xtouch {
  $contents = Get-ChildItem
  foreach ($file in $contents) {
    if ($file.Attributes -eq 'Directory') {
      echo ">>> Entering directory $($file.Name)"
      cd $file
      xtouch
      echo "<<< Leaving directory $($file.Name)"
      cd ..
    } else {
      $file.LastAccessTime = (Get-Date)
      echo "Touch $($file.Name): $($file.LastAccessTime)"
    }
  }
}

xtouch
