from trak import TRAKer

def get_attrib_matrix(train_dl, val_dl, model, ckpts, train_set_size, val_set_size, **kwargs):
    if kwargs is None or kwargs.get('task') is None:
        task = 'image_classification'
    else:
        task = kwargs.pop('task')

    traker = TRAKer(
        model=model,
        task=task,
        train_set_size=train_set_size,
        **kwargs)

    for model_id, checkpoint in enumerate(ckpts):
        traker.load_checkpoint(checkpoint, model_id=model_id)
        for batch in loader_train:
            batch = [x.cuda() for x in batch]
            # batch should be a tuple/list of inputs and labels
            traker.featurize(batch=batch, num_samples=batch[0].shape[0])

    traker.finalize_features()

    for model_id, checkpoint in enumerate(checkpoints):
        traker.start_scoring_checkpoint(checkpoint,
                                        model_id=model_id,
                                        exp_name='test',
                                        num_targets=val_set_size)
    for batch in targets_loader:
        batch = [x.cuda() for x in batch]
        traker.score(batch=batch, num_samples=batch[0].shape[0])

    scores = traker.finalize_scores(exp_name='test')
    return scores