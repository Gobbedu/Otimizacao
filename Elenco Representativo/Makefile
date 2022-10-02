# Eduardo Gobbo Willi Vasconcellos Goncalves GRR20203892

APP = elenco.py
EXEC = elenco

# COMMAND LINE OPTIONS
# -a : limitante dada
# -o : corte otimalidade desabilitado (limitante)
# -f : corte viabilidade desabilitado

all: $(EXEC)

$(EXEC): $(APP) 
	@cp $< $@
	@chmod +x $@

clean:
	@rm -f $(EXEC)
	@rm -rf __pycache__

run: clean $(EXEC) 
# 	sem nenhum tipo de pruning
# ./$(EXEC) -o -f		< testes/richard.txt
# 	com bound dado
# ./$(EXEC) -a -f	< testes/richard.txt
# 	com bound proprio
# ./$(EXEC) -f	< testes/richard.txt
# 	com viabilidade
# ./$(EXEC) -o 	< testes/richard.txt
# 	viabilidade e bound dado
# ./$(EXEC) -a	< testes/richard.txt
# 	viabilidade e bound proprio
# ./$(EXEC) 	< testes/richard.txt

