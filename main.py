import docker

CLIENT = docker.from_env()


def list_images():
    print('\n    ID:\t\t\tNAME:')
    for image in CLIENT.images.list(all=True):
        for image_tag in image.tags:
            print(image.short_id[7:], '\t', image_tag)
    print('\n')


def list_containers():
    print('\nID:\t\t\tNAME:\t\t\tIMAGE:')
    for container in CLIENT.containers.list(all=True):
        print('{}\t{}\t{}'.format(container.short_id, container.name.rjust(25), container.image))
    print('\n')


def pull_image():
    repo_list = ['1', '2', '3', 'Q', 'q']
    image_name = ''
    chosen_repo = ''
    while chosen_repo not in repo_list:
        chosen_repo = input(f'''
        Please select one of the following repositories:
        {'-' * 69}
        1 - Debian; 2 - Ubuntu; 3 - CentOS; 4- Fedora, 5 - Mageia, 6 - Alpine
        {'-' * 69}
        Please use numeric digits: from 1 to 6 only.
        Or just type "Q/q" to quit from the function\n
        ''')
        if chosen_repo == 'Q' or 'q':
            break
    if chosen_repo == '1':
        image_name = 'debian'
    elif chosen_repo == '2':
        image_name = 'ubuntu'
    elif chosen_repo == '3':
        image_name = 'centos'
    elif chosen_repo == '4':
        image_name = 'fedora'
    elif chosen_repo == '5':
        image_name = 'mageia'
    elif chosen_repo == '6':
        image_name = 'alpine'
    CLIENT.images.pull(image_name)
    print(f'The image {image_name} has been pulled, and been added to the list:\n')
    list_images()


def delete_image():
    print('To delete, please copy/paste one of the listed image IDs:\n')
    list_images()
    image_id = input('Delete image by image ID:\n').strip()
    CLIENT.images.remove(image_id)
    print(f'The selected image {image_id} has been removed.\nThe updated image list\n')
    list_images()


def run_container():
    print('To run a new container, please copy/paste one of the listed image IDs:\n')
    list_images()
    image_id = input('Select the image to run a new container:\n').strip()
    CLIENT.container.run(image_id)
    print(f'Running container from the selected image {image_id}\n')
    list_containers()


def stop_container(): ##TODO: add check if there is running container
    running_filter = {'status': 'running'}
    CLIENT.containers.list(filters=running_filter)
    container_name = input('Select the container name to stop: ').strip()
    for container in CLIENT.containers.list(filters=running_filter):
        print(f'\tStopping container:\tID\t{container.short_id}\tNAME:\t{container.name}')
        container.stop()
        print(f'The container {container_name} has been stopped.')
    list_containers()


def delete_container():
    list_containers()
    container_name = input('Select the container name to delete: ').strip()
    exited_filter = {'status': 'exited', 'name': container_name}
    print('\nFiltered containers:')
    for container in CLIENT.containers.list(filters=exited_filter):
        print(f'\tRemoving container:\tID\t{container.short_id}\tNAME:\t{container.name}')
        container.stop()
        container.remove()
        print('\t...successfully removed')
    list_containers()


def main():
    actions = {
        'q': quit,
        'li': list_images,
        'lc': list_containers,
        'pi': pull_image,
        'di': delete_image,
        'rc': run_container,
        'sc': stop_container,
        'dc': delete_container
    }
    while True:
        choice = input(f'''
        Please input command\n\t{'-' * 25}
        'q': quit,
        'li': list all images,
        'lc': list all containers,
        'pi': pull new image,
        'di': delete image,
        'rc': run container,
        'sc': stop container,
        'dc': delete container\n\t{'-' * 25}
        ''').lower()
        if choice in actions.keys():
           actions[choice]()
        else:
            print('Invalid input. Please try again')


if __name__ == '__main__':
    main()
