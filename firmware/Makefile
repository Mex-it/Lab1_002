# A very simple makefile full of shortcuts

# What port the arduino is on
ifndef SERIAL_DEV
	ifneq (,$(wildcard /dev/ttyUSB0))
		SERIAL_DEV = /dev/ttyUSB0
	else ifneq (,$(wildcard /dev/ttyACM0))
		SERIAL_DEV = /dev/ttyACM0
	else
		SERIAL_DEV = unknown
	endif
endif

.PHONY: build test

ALL: build

build:
	pio run

# For CI
binaries:
	pio run
	pio run -t .pio/build/megaatmega2560/firmware.eep

flash:
	pio run -t upload

deep:
	pio run -t uploadeep

clean:
	pio run -t clean
	git clean -fdx

lint:
	pio check

test:
	pio test --upload-port $(SERIAL_DEV)

debug: flash monitor

monitor:
	pio device monitor --filter=direct --filter=time

# Remote versions of the above
flash-remote:
	pio remote --agent silvertech-desk run --target upload --upload-port /dev/ttyACM0

monitor-remote:
	pio remote --agent silvertech-desk device monitor -p /dev/ttyACM0

debug-remote: flash-remote monitor-remote
