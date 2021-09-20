MODELS = pic16f886 pic16f887
HEADERS = $(MODELS:%=%.h)

default: $(HEADERS)

$(HEADERS): codegen.py
	./codegen.py $(@:%.h=%) > $@
