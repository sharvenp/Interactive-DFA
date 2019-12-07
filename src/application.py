
from view import View
from dfa import DFA
from controller import Controller

if __name__ == '__main__':
	
	view = View()
	dfa = DFA()
	controller = Controller()

	# MVC
	dfa.add_observer(view)
	view.attach_controller(controller)
	controller.set_model(dfa)

	# Launch Application
	view.launch()