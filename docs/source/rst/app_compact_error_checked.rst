=========
BLUESTORM
=========

check_access
============

.. code-block:: python

   def check_access(current_user):	
       '''

        Controla se usuario que esta usando o sistema e um usuario ativo 


        param current_user : string
        param current_user : Usuario logado no sistema
        returns : Message  

		'''
	    return jsonify({message': 'Acesso nao autorizado'})
