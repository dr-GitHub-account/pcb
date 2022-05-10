# dataset settings
dataset_type = 'PCBDataset'
data_root = '/home/user/xiongdengrui/pcb/DeepPCB/PCBData_collected/'
classes = ('open', 'short', 'mousebite', 'spur', 'copper', 'pin-hole')
img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True)

train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(type='Resize', img_scale=(800, 800), keep_ratio=True),
    # dict(type='Resize', img_scale=(896, 896), keep_ratio=True),
    dict(type='RandomFlip', flip_ratio=0.5),
    # dict(
    #     type='RandomFlip',
    #     flip_ratio=[0.25, 0.25, 0.25],
    #     direction=['horizontal', 'vertical', 'diagonal']),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='Pad', size_divisor=32),
    dict(type='DefaultFormatBundle'),
    dict(type='Collect', keys=['img', 'gt_bboxes', 'gt_labels']),
]

test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='MultiScaleFlipAug',
        img_scale=(800, 800),
        # img_scale=(896, 896),
        flip=False,
        transforms=[
            dict(type='Resize', keep_ratio=True),
            dict(type='RandomFlip'),
            dict(type='Normalize', **img_norm_cfg),
            dict(type='Pad', size_divisor=32),
            dict(type='ImageToTensor', keys=['img']),
            dict(type='Collect', keys=['img']),
        ])
]
# data = dict(
#     samples_per_gpu=2,
#     workers_per_gpu=2,
#     train=dict(
#         type=dataset_type,
#         classes=classes,
#         # ann_file=data_root + 'annotations/train.json',
#         ann_file=data_root + 'annotations/instances_all.json',
#         img_prefix=data_root + '/images/train_data/',
#         pipeline=train_pipeline),
#     val=dict(
#         type=dataset_type,
#         classes=classes,
#         ann_file=data_root + 'annotations/val.json',
#         img_prefix=data_root + '/images/train_data/',
#         pipeline=test_pipeline),
#     test=dict(
#         type=dataset_type,
#         classes=classes,
#         ann_file=data_root + 'annotations/test.json',
#         img_prefix=data_root + '/images/test_data/',
#         pipeline=test_pipeline))
data = dict(
    samples_per_gpu=1,
    workers_per_gpu=2,
    train=dict(
        type=dataset_type,
        # ann_file=data_root + 'annotations/instances_train2017.json',
        # img_prefix=data_root + 'train2017/',
        ann_file=data_root + 'anno_json/trainval.json',
        img_prefix=data_root + 'images_defect/',
        pipeline=train_pipeline),
    val=dict(
        type=dataset_type,
        # ann_file=data_root + 'annotations/instances_val2017.json',
        # img_prefix=data_root + 'val2017/',
        ann_file=data_root + 'anno_json/test.json',
        img_prefix=data_root + 'images_defect/',
        pipeline=test_pipeline),
    test=dict(
        type=dataset_type,
        # ann_file=data_root + 'annotations/instances_val2017.json',
        # img_prefix=data_root + 'val2017/',
        ann_file=data_root + 'anno_json/test.json',
        img_prefix=data_root + 'images_defect/',
        pipeline=test_pipeline))
# evaluation = dict(interval=1, metric='bbox')