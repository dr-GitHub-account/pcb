time=$(date "+%Y%m%d%H%M%S")
work_folder=./work_dir/${time}
# config_folder='./configs/faster_rcnn/'

# CUDA_VISIBLE_DEVICES=0,1 bash ./tools/dist_train.sh \
#     /home/user/xiongdengrui/pcb/mmdetection/configs/faster_rcnn/faster_rcnn_r50_fpn_1x_coco.py \
#     2 \
#     --work-dir ./${work_folder}/${method}/

python /home/user/xiongdengrui/pcb/mmdetection/tools/train.py \
    /home/user/xiongdengrui/pcb/mmdetection/configs/faster_rcnn/faster_rcnn_r50_fpn_1x_coco.py \
    --work-dir ./${work_folder}/ \
    --gpu-ids 1