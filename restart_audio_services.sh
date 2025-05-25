#!/bin/bash
#
# Restarts user-level audio services (PipeWire, WirePlumber).

systemctl --user restart wireplumber pipewire.service pipewire-pulse.service