// Mostrar opções de votação quando o mouse passa sobre o botão
    $("#vote-button").mouseenter(function(){
        $("#voting-options").show();
    });

    // Ocultar opções de votação quando o mouse deixa o contêiner
    $("#voting-container").mouseleave(function(){
        $("#voting-options").hide();
    });

    // Enviar voto ao clicar em uma opção
    $(".vote-option").click(function(){
        var voteType = $(this).data("vote-type");
        var contentId = $(this).data("content-id");


        // Atualizar ícone no botão de votação
        switch(voteType) {
            case "like":
                $("#vote-button").html('<i class="bi bi-hand-thumbs-up-fill"></i>');
                break;
            case "heart":
                $("#vote-button").html('<i class="bi bi-heart-fill"></i>');
                break;
            case "bomb":
                $("#vote-button").html('<i class="bi bi-lightning-charge-fill"></i>');
                break;
            case "must":
                $("#vote-button").html('<i class="bi bi-asterisk"></i>');
                break;
            // Adicione casos para outros tipos de votos, se necessário
        }
        
        // Enviar voto via AJAX
        $.ajax({
            url: '/init/toca/vote/' + contentId + '/' + voteType ,
            type: 'post',
            data: {
                content_id: contentId,
                vote_type: voteType,
                // Outros dados necessários
            },
            success: function(response){
                // Tratar a resposta do servidor
                $("#voting-options").hide();
                web2py_component("/init/toca/load_votes/"+contentId, 'vote-button')
            }
        });
    });
