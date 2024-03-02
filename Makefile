ifeq ($(OS),Windows_NT)
    NULL := NUL
    RM := rmdir /s /q
else
    NULL := /dev/null
    RM := rm -rf
endif

publish:
	pyinstaller pyinstaller.spec
	$(RM) build > $(NULL)