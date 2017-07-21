# SmoothCriminal
Detect sandbox by cursor movement speed

## About
This tool was created as a demonstration for my talk about vaccination @ BSdiesLV 2017.
It is an example for a simple technique to bypass many sandboxes by monitoring mouse movements.
While many tools and malware looks if the mouse moved at all, my tool checks if the movement was smooth by applying basic calculus.
There are some thresholds I set in advance - feel free to play with it.
Will be glad to get your feedback @ https://twitter.com/Gal_B1t

## Goal
My aim is to show that there are many ways to create new evasion techniques, yet, like this one - most of them can be easily countered.

## HOWTO
### Mean Mode
Execute with the flag -mean
The script will accumulate the mouse speed values (only if a movement occurred) and will return the average of all speeds.
In a sandbox, the cursor only jumps so the average will be much higher.

### Max Mode
Execute with the flag -max
It will run similarly, yet instead of the average it will return the maximal speed.
This technique can trigger a false positive if a flesh and blood user moves its cursor extremely fast.

## Disclaimer
This tool and its abstract logic should be used only for legal and educational purposes.
Anyone adopting ir adapting it for illegale purposes is doing so at its own risk.

## License
CC-BY-SA
https://creativecommons.org/licenses/by-sa/2.0/
